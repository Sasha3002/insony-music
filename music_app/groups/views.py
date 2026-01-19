from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Group, GroupMembership, GroupInvitation
from music.models import Genre
from django.contrib.auth import get_user_model
import requests
from time import sleep
from django.utils import timezone

User = get_user_model()

@login_required
def group_list(request):
    groups = Group.objects.annotate(
        members_count=Count('members', filter=Q(members__status='accepted'))
    ).select_related('admin').prefetch_related('genres')
    
    # Search by name
    query = request.GET.get('q', '')
    if query:
        groups = groups.filter(name__icontains=query)

    location = request.GET.get('location', '')
    if location:
        groups = groups.filter(location__icontains=location)

    genre_id = request.GET.get('genre', '')
    if genre_id:
        groups = groups.filter(genres__id=genre_id)
    
    # Get all genres for filter dropdown
    all_genres = Genre.objects.all()

    invitation_count = GroupInvitation.objects.filter(
        invited_user=request.user,
        accepted=False
    ).count()
    
    return render(request, 'groups/group_list.html', {
        'groups': groups,
        'all_genres': all_genres,
        'query': query,
        'location': location,
        'selected_genre': genre_id,
        'invitation_count': invitation_count,
    })


@login_required
def group_detail(request, slug):
    group = get_object_or_404(Group.objects.prefetch_related('genres', 'members__user'), slug=slug)
    is_member = group.members.filter(user=request.user, status='accepted').exists()
    is_admin = group.admin == request.user
    has_pending_request = group.members.filter(user=request.user, status='pending').exists()
    members = group.members.filter(status='accepted').select_related('user')
    pending_requests = []
    if is_admin:
        pending_requests = group.members.filter(status='pending').select_related('user')

    now = timezone.now()
    
    upcoming_events = []
    past_events = []
    
    for event in group.events.all().select_related('creator').prefetch_related('attendees'):
        if event.is_past:
            past_events.append(event)
        else:
            upcoming_events.append(event)
    
    # Sort events
    upcoming_events.sort(key=lambda x: x.event_date)
    past_events.sort(key=lambda x: x.event_date, reverse=True)
    
    return render(request, 'groups/group_detail.html', {
        'group': group,
        'is_member': is_member,
        'is_admin': is_admin,
        'has_pending_request': has_pending_request,
        'members': members,
        'pending_requests': pending_requests,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    })

def validate_city(city_name):
    if not city_name:
        return False
    
    if city_name.lower() == 'online':
        return True
    
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'city': city_name,
            'country': 'Poland',
            'format': 'json',
            'limit': 1
        }
        headers = {
            'User-Agent': 'Insony/1.0 (Music Community Platform)'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return len(data) > 0
        return False
        
    except Exception as e:
        print(f"Location validation error: {e}")
        return True


@login_required
def group_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        location = request.POST.get('location')
        type = request.POST.get('type', 'public')
        cover_image = request.FILES.get('cover_image')
        genre_ids = request.POST.getlist('genres')
        
        if not name or not description or not location:
            messages.error(request, 'Wszystkie pola są wymagane')
            return redirect('group_create')
        
        # Validate location
        if not validate_city(location):
            messages.error(request, f'Lokalizacja "{location}" nie istnieje w Polsce. Sprawdź pisownię lub wpisz "Online".')
            genres = Genre.objects.all()
            return render(request, 'groups/group_create.html', {
                'genres': genres,
                'submitted_data': request.POST  
            })
        
        group = Group.objects.create(
            name=name,
            description=description,
            location=location,
            type=type,
            admin=request.user,
            cover_image=cover_image
        )
        
        if genre_ids:
            group.genres.set(genre_ids)
        
        GroupMembership.objects.create(
            group=group,
            user=request.user,
            status='accepted'
        )
        
        messages.success(request, f'Grupa "{name}" została utworzona!')
        return redirect('group_detail', slug=group.slug)
    
    genres = Genre.objects.all()
    return render(request, 'groups/group_create.html', {
        'genres': genres
    })


@login_required
def group_edit(request, slug):
    group = get_object_or_404(Group, slug=slug)
    
    if group.admin != request.user:
        messages.error(request, 'Tylko administrator może edytować grupę')
        return redirect('group_detail', slug=slug)
    
    if request.method == 'POST':
        group.location = request.POST.get('location')
        # Validate location
        if not validate_city(group.location):
            messages.error(request, f'Lokalizacja "{group.location}" nie istnieje w Polsce. Sprawdź pisownię lub wpisz "Online".')
            genres = Genre.objects.all()
            return render(request, 'groups/group_edit.html', {
                'group': group,
                'genres': genres
            })

        group.name = request.POST.get('name')
        group.description = request.POST.get('description')
        group.type = request.POST.get('type', 'public')
        
        if 'cover_image' in request.FILES:
            if group.cover_image:
                group.cover_image.delete()  
            group.cover_image = request.FILES['cover_image']
        
        genre_ids = request.POST.getlist('genres')
        
        group.save()
        
        if genre_ids:
            group.genres.set(genre_ids)
        
        messages.success(request, 'Grupa została zaktualizowana')
        return redirect('group_detail', slug=group.slug)
    
    genres = Genre.objects.all()
    return render(request, 'groups/group_edit.html', {
        'group': group,
        'genres': genres
    })


@login_required
def group_delete(request, slug):
    group = get_object_or_404(Group, slug=slug)
    
    if group.admin != request.user:
        messages.error(request, 'Tylko administrator może usunąć grupę')
        return redirect('group_detail', slug=slug)
    
    if request.method == 'POST':
        group_name = group.name
        group.delete()
        messages.success(request, f'Grupa "{group_name}" została usunięta')
        return redirect('group_list')
    
    return render(request, 'groups/group_delete_confirm.html', {
        'group': group
    })


@require_POST
@login_required
def group_join(request, slug):
    group = get_object_or_404(Group, slug=slug)
    existing = GroupMembership.objects.filter(group=group, user=request.user).first()
    
    if existing:
        if existing.status == 'accepted':
            messages.info(request, 'Już jesteś członkiem tej grupy')
        elif existing.status == 'pending':
            messages.info(request, 'Twoja prośba o dołączenie oczekuje na akceptację')
        return redirect('group_detail', slug=slug)
    
    status = 'accepted' if group.type == 'public' else 'pending'
    GroupMembership.objects.create(
        group=group,
        user=request.user,
        status=status
    )
    
    if status == 'accepted':
        messages.success(request, f'Dołączyłeś do grupy "{group.name}"')
    else:
        messages.success(request, 'Prośba o dołączenie została wysłana')
    
    return redirect('group_detail', slug=slug)


@require_POST
@login_required
def group_leave(request, slug):
    group = get_object_or_404(Group, slug=slug)
    
    if group.admin == request.user:
        messages.error(request, 'Administrator nie może opuścić grupy. Usuń grupę lub przekaż administrację.')
        return redirect('group_detail', slug=slug)
    
    membership = GroupMembership.objects.filter(group=group, user=request.user).first()
    
    if membership:
        membership.delete()
        messages.success(request, f'Opuściłeś grupę "{group.name}"')
    
    return redirect('group_list')


@require_POST
@login_required
def approve_member(request, slug, membership_id):
    group = get_object_or_404(Group, slug=slug)
    
    if group.admin != request.user:
        messages.error(request, 'Tylko administrator może akceptować członków')
        return redirect('group_detail', slug=slug)
    
    membership = get_object_or_404(GroupMembership, id=membership_id, group=group)
    membership.status = 'accepted'
    membership.save()
    
    messages.success(request, f'{membership.user.username} został zaakceptowany')
    return redirect('group_detail', slug=slug)


@require_POST
@login_required
def reject_member(request, slug, membership_id):
    group = get_object_or_404(Group, slug=slug)
    
    if group.admin != request.user:
        messages.error(request, 'Tylko administrator może odrzucać członków')
        return redirect('group_detail', slug=slug)
    
    membership = get_object_or_404(GroupMembership, id=membership_id, group=group)
    membership.delete()
    
    messages.success(request, f'Prośba od {membership.user.username} została odrzucona')
    return redirect('group_detail', slug=slug)


@login_required
def group_invite(request, slug):
    group = get_object_or_404(Group, slug=slug)

    if not group.members.filter(user=request.user, status='accepted').exists():
        messages.error(request, 'Tylko członkowie mogą zapraszać')
        return redirect('group_detail', slug=slug)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        user_to_invite = User.objects.filter(username=username).first()
        
        if not user_to_invite:
            messages.error(request, 'Użytkownik nie istnieje')
            return redirect('group_invite', slug=slug)
        
        if group.members.filter(user=user_to_invite).exists():
            messages.error(request, 'Użytkownik już jest członkiem lub ma oczekującą prośbę')
            return redirect('group_invite', slug=slug)
        
        if GroupInvitation.objects.filter(group=group, invited_user=user_to_invite).exists():
            messages.error(request, 'Zaproszenie już zostało wysłane')
            return redirect('group_invite', slug=slug)
        
        GroupInvitation.objects.create(
            group=group,
            invited_by=request.user,
            invited_user=user_to_invite
        )
        
        messages.success(request, f'Zaproszenie wysłane do {username}')
        return redirect('group_detail', slug=slug)
    
    return render(request, 'groups/group_invite.html', {
        'group': group
    })


@login_required
def group_members(request, slug):
    group = get_object_or_404(Group, slug=slug)
    members = group.members.filter(status='accepted').select_related('user')
    is_admin = group.admin == request.user
    
    return render(request, 'groups/group_members.html', {
        'group': group,
        'members': members,
        'is_admin': is_admin,
    })

@require_POST
@login_required
def remove_member(request, slug, user_id):
    group = get_object_or_404(Group, slug=slug)
    
    if group.admin != request.user:
        messages.error(request, 'Tylko administrator może usuwać członków')
        return redirect('group_detail', slug=slug)
    
    user_to_remove = get_object_or_404(User, id=user_id)
    
    if user_to_remove == group.admin:
        messages.error(request, 'Administrator nie może usunąć samego siebie')
        return redirect('group_detail', slug=slug)
    
    membership = GroupMembership.objects.filter(group=group, user=user_to_remove).first()
    
    if membership:
        membership.delete()
        messages.success(request, f'{user_to_remove.username} został usunięty z grupy')
    else:
        messages.error(request, 'Użytkownik nie jest członkiem grupy')
    return redirect('group_detail', slug=slug)

@login_required
def my_invitations(request):
    invitations = GroupInvitation.objects.filter(
        invited_user=request.user,
        accepted=False
    ).select_related('group', 'invited_by').order_by('-created_at')
    
    return render(request, 'groups/my_invitations.html', {
        'invitations': invitations
    })


@require_POST
@login_required
def accept_invitation(request, invitation_id):
    invitation = get_object_or_404(GroupInvitation, id=invitation_id, invited_user=request.user)

    if GroupMembership.objects.filter(group=invitation.group, user=request.user).exists():
        messages.info(request, 'Już jesteś członkiem tej grupy')
        invitation.delete()
        return redirect('my_invitations')
    
    GroupMembership.objects.create(
        group=invitation.group,
        user=request.user,
        status='accepted'
    )
    
    invitation.accepted = True
    invitation.save()
    invitation.delete()
    
    messages.success(request, f'Dołączyłeś do grupy "{invitation.group.name}"')
    return redirect('group_detail', slug=invitation.group.slug)


@require_POST
@login_required
def decline_invitation(request, invitation_id):
    invitation = get_object_or_404(GroupInvitation, id=invitation_id, invited_user=request.user)
    group_name = invitation.group.name
    invitation.delete()
    
    messages.success(request, f'Odrzuciłeś zaproszenie do grupy "{group_name}"')
    return redirect('my_invitations')