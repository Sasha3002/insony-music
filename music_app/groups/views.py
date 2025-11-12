from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Group, GroupMembership, GroupInvitation
from music.models import Genre
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def group_list(request):
    """List all groups with search and filters"""
    groups = Group.objects.annotate(
        members_count=Count('members', filter=Q(members__status='accepted'))
    ).select_related('admin').prefetch_related('genres')
    
    # Search by name
    query = request.GET.get('q', '')
    if query:
        groups = groups.filter(name__icontains=query)
    
    # Filter by location
    location = request.GET.get('location', '')
    if location:
        groups = groups.filter(location__icontains=location)
    
    # Filter by genre
    genre_id = request.GET.get('genre', '')
    if genre_id:
        groups = groups.filter(genres__id=genre_id)
    
    # Get all genres for filter dropdown
    all_genres = Genre.objects.all()
    
    return render(request, 'groups/group_list.html', {
        'groups': groups,
        'all_genres': all_genres,
        'query': query,
        'location': location,
        'selected_genre': genre_id,
    })


@login_required
def group_detail(request, slug):
    """View group details"""
    group = get_object_or_404(Group.objects.prefetch_related('genres', 'members__user'), slug=slug)
    
    # Check if user is member
    is_member = group.members.filter(user=request.user, status='accepted').exists()
    is_admin = group.admin == request.user
    
    # Check if user has pending request
    has_pending_request = group.members.filter(user=request.user, status='pending').exists()
    
    # Get accepted members
    members = group.members.filter(status='accepted').select_related('user')
    
    # Get pending requests (only visible to admin)
    pending_requests = []
    if is_admin:
        pending_requests = group.members.filter(status='pending').select_related('user')
    
    return render(request, 'groups/group_detail.html', {
        'group': group,
        'is_member': is_member,
        'is_admin': is_admin,
        'has_pending_request': has_pending_request,
        'members': members,
        'pending_requests': pending_requests,
    })


@login_required
def group_create(request):
    """Create a new group"""
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
        
        # Create group
        group = Group.objects.create(
            name=name,
            description=description,
            location=location,
            type=type,
            admin=request.user,
            cover_image=cover_image
        )
        
        # Add genres
        if genre_ids:
            group.genres.set(genre_ids)
        
        # Auto-add creator as member
        GroupMembership.objects.create(
            group=group,
            user=request.user,
            status='accepted'
        )
        
        messages.success(request, f'Grupa "{name}" została utworzona!')
        return redirect('group_detail', slug=group.slug)
    
    # GET request
    genres = Genre.objects.all()
    return render(request, 'groups/group_create.html', {
        'genres': genres
    })


@login_required
def group_edit(request, slug):
    """Edit group (admin only)"""
    group = get_object_or_404(Group, slug=slug)
    
    if group.admin != request.user:
        messages.error(request, 'Tylko administrator może edytować grupę')
        return redirect('group_detail', slug=slug)
    
    if request.method == 'POST':
        group.name = request.POST.get('name')
        group.description = request.POST.get('description')
        group.location = request.POST.get('location')
        group.type = request.POST.get('type', 'public')
        
        if request.FILES.get('cover_image'):
            group.cover_image = request.FILES.get('cover_image')
        
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
    """Delete group (admin only)"""
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
    """Join a group"""
    group = get_object_or_404(Group, slug=slug)
    
    # Check if already member
    existing = GroupMembership.objects.filter(group=group, user=request.user).first()
    
    if existing:
        if existing.status == 'accepted':
            messages.info(request, 'Już jesteś członkiem tej grupy')
        elif existing.status == 'pending':
            messages.info(request, 'Twoja prośba o dołączenie oczekuje na akceptację')
        return redirect('group_detail', slug=slug)
    
    # Create membership
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
    """Leave a group"""
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
    """Approve pending member (admin only)"""
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
    """Reject pending member (admin only)"""
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
    """Invite users to group"""
    group = get_object_or_404(Group, slug=slug)
    
    # Only members can invite
    if not group.members.filter(user=request.user, status='accepted').exists():
        messages.error(request, 'Tylko członkowie mogą zapraszać')
        return redirect('group_detail', slug=slug)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        user_to_invite = User.objects.filter(username=username).first()
        
        if not user_to_invite:
            messages.error(request, 'Użytkownik nie istnieje')
            return redirect('group_invite', slug=slug)
        
        # Check if already member or invited
        if group.members.filter(user=user_to_invite).exists():
            messages.error(request, 'Użytkownik już jest członkiem lub ma oczekującą prośbę')
            return redirect('group_invite', slug=slug)
        
        if GroupInvitation.objects.filter(group=group, invited_user=user_to_invite).exists():
            messages.error(request, 'Zaproszenie już zostało wysłane')
            return redirect('group_invite', slug=slug)
        
        # Create invitation
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
    """View all group members"""
    group = get_object_or_404(Group, slug=slug)
    members = group.members.filter(status='accepted').select_related('user')
    
    return render(request, 'groups/group_members.html', {
        'group': group,
        'members': members
    })