from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Q, Count
from django.utils import timezone
from .models import Event, EventAttendee, EventRating
from groups.models import Group, GroupMembership
from datetime import datetime


@login_required
def event_list(request):
    """List all upcoming events"""
    now = timezone.now()
    
    # Get filter parameters
    filter_type = request.GET.get('filter', 'upcoming')
    city_filter = request.GET.get('city', '')
    
    if filter_type == 'past':
        events = Event.objects.filter(event_date__lt=now)
    elif filter_type == 'my':
        # Events from groups user is member of
        user_groups = Group.objects.filter(members__user=request.user, members__status='accepted')
        events = Event.objects.filter(group__in=user_groups)
    else:  # upcoming (default)
        events = Event.objects.filter(event_date__gte=now)
    
    # Filter by city (from group location)
    if city_filter:
        events = events.filter(group__location__icontains=city_filter)
    
    events = events.select_related('group', 'creator').prefetch_related('attendees').order_by('event_date')
    
    # Get unique cities from groups that have events
    cities = Group.objects.filter(
        events__isnull=False
    ).values_list('location', flat=True).distinct().order_by('location')
    
    return render(request, 'events/event_list.html', {
        'events': events,
        'filter_type': filter_type,
        'city_filter': city_filter,
        'cities': cities,
    })

@login_required
def event_detail(request, slug):
    """View event details"""
    event = get_object_or_404(Event.objects.select_related('group', 'creator'), slug=slug)
    
    # Check if user is group member
    is_member = GroupMembership.objects.filter(
        group=event.group,
        user=request.user,
        status='accepted'
    ).exists()
    
    # Check user's attendance status
    user_attendance = None
    if is_member:
        user_attendance = EventAttendee.objects.filter(
            event=event,
            user=request.user
        ).first()
    
    # Get attendees
    attendees = event.attendees.filter(status='going').select_related('user')
    
    is_creator = event.creator == request.user
    is_admin = event.group.admin == request.user

    user_rating = None
    can_rate = False
    
    if event.is_past and user_attendance and user_attendance.status == 'going':
        can_rate = True
        user_rating = EventRating.objects.filter(event=event, user=request.user).first()
    
    # Get all ratings
    ratings = event.ratings.select_related('user').order_by('-created_at')
    
    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_member': is_member,
        'is_creator': is_creator,
        'is_admin': is_admin,
        'user_attendance': user_attendance,
        'attendees': attendees,
        'can_rate': can_rate,
        'user_rating': user_rating,
        'ratings': ratings,
    })


@login_required
def event_create(request, group_slug):
    """Create a new event for a group"""
    group = get_object_or_404(Group, slug=group_slug)
    
    # Check if user is a member
    if not GroupMembership.objects.filter(group=group, user=request.user, status='accepted').exists():
        messages.error(request, 'Tylko członkowie grupy mogą tworzyć wydarzenia')
        return redirect('group_detail', slug=group_slug)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        event_date_str = request.POST.get('event_date')
        end_date_str = request.POST.get('end_date', '').strip()
        event_image = request.FILES.get('event_image')
        
        if not all([title, description, location, event_date_str]):
            messages.error(request, 'Wszystkie wymagane pola muszą być wypełnione')
            return redirect('event_create', group_slug=group_slug)
        
        # Convert datetime strings to timezone-aware datetimes
        try:
            event_date = timezone.make_aware(datetime.fromisoformat(event_date_str))
            end_date = timezone.make_aware(datetime.fromisoformat(end_date_str)) if end_date_str else None
        except ValueError:
            messages.error(request, 'Nieprawidłowy format daty')
            return redirect('event_create', group_slug=group_slug)
        
        # Create event
        event = Event.objects.create(
            group=group,
            creator=request.user,
            title=title,
            description=description,
            location=location,
            event_date=event_date,
            end_date=end_date,
            event_image=event_image
        )
        
        # Auto-add creator as attendee
        EventAttendee.objects.create(
            event=event,
            user=request.user,
            status='going'
        )
        
        messages.success(request, f'Wydarzenie "{title}" zostało utworzone!')
        return redirect('event_detail', slug=event.slug)
    
    return render(request, 'events/event_create.html', {
        'group': group
    })


@login_required
def event_edit(request, slug):
    """Edit event (creator or group admin only)"""
    event = get_object_or_404(Event, slug=slug)
    
    # Check permissions
    if event.creator != request.user and event.group.admin != request.user:
        messages.error(request, 'Tylko twórca wydarzenia lub administrator grupy może je edytować')
        return redirect('event_detail', slug=slug)
    
    if request.method == 'POST':
        event.title = request.POST.get('title')
        event.description = request.POST.get('description')
        event.location = request.POST.get('location')
        event.event_date = request.POST.get('event_date')
        event.end_date = request.POST.get('end_date', '').strip() or None
        
        # Handle image update
        if 'event_image' in request.FILES:
            if event.event_image:
                event.event_image.delete()
            event.event_image = request.FILES['event_image']
        
        event.save()
        
        messages.success(request, 'Wydarzenie zostało zaktualizowane')
        return redirect('event_detail', slug=event.slug)
    
    return render(request, 'events/event_edit.html', {
        'event': event
    })


@login_required
def event_delete(request, slug):
    """Delete event (creator or group admin only)"""
    event = get_object_or_404(Event, slug=slug)
    
    # Check permissions
    if event.creator != request.user and event.group.admin != request.user:
        messages.error(request, 'Tylko twórca wydarzenia lub administrator grupy może je usunąć')
        return redirect('event_detail', slug=slug)
    
    if request.method == 'POST':
        event_title = event.title
        group_slug = event.group.slug
        event.delete()
        messages.success(request, f'Wydarzenie "{event_title}" zostało usunięte')
        return redirect('group_detail', slug=group_slug)
    
    return render(request, 'events/event_delete_confirm.html', {
        'event': event
    })


@require_POST
@login_required
def event_attend(request, slug):
    """Mark attendance for an event"""
    event = get_object_or_404(Event, slug=slug)
    status = request.POST.get('status', 'going')
    
    # Check if user is group member
    if not GroupMembership.objects.filter(group=event.group, user=request.user, status='accepted').exists():
        messages.error(request, 'Tylko członkowie grupy mogą uczestniczyć w wydarzeniach')
        return redirect('event_detail', slug=slug)
    
    # Get or create attendance
    attendance, created = EventAttendee.objects.get_or_create(
        event=event,
        user=request.user,
        defaults={'status': status}
    )
    
    if not created:
        if attendance.status == status:
            # Remove attendance if clicking same status
            attendance.delete()
            messages.info(request, 'Anulowano uczestnictwo')
        else:
            # Update status
            attendance.status = status
            attendance.save()
            status_text = dict(EventAttendee.STATUS_CHOICES)[status]
            messages.success(request, f'Status zaktualizowany: {status_text}')
    else:
        status_text = dict(EventAttendee.STATUS_CHOICES)[status]
        messages.success(request, f'Status: {status_text}')
    
    return redirect('event_detail', slug=slug)

@require_POST
@login_required
def rate_event(request, slug):
    """Rate a past event"""
    event = get_object_or_404(Event, slug=slug)
    
    # Check if event is past
    if not event.is_past:
        messages.error(request, 'Możesz ocenić tylko zakończone wydarzenia')
        return redirect('event_detail', slug=slug)
    
    # Check if user attended the event
    attended = EventAttendee.objects.filter(
        event=event,
        user=request.user,
        status='going'
    ).exists()
    
    if not attended:
        messages.error(request, 'Możesz ocenić tylko wydarzenia, w których uczestniczyłeś')
        return redirect('event_detail', slug=slug)
    
    rating_value = request.POST.get('rating')
    comment = request.POST.get('comment', '').strip()
    
    if not rating_value:
        messages.error(request, 'Musisz wybrać ocenę')
        return redirect('event_detail', slug=slug)
    
    try:
        rating_value = int(rating_value)
        if rating_value < 1 or rating_value > 5:
            raise ValueError
    except ValueError:
        messages.error(request, 'Nieprawidłowa ocena')
        return redirect('event_detail', slug=slug)
    
    # Create or update rating
    rating, created = EventRating.objects.update_or_create(
        event=event,
        user=request.user,
        defaults={
            'rating': rating_value,
            'comment': comment
        }
    )
    
    if created:
        messages.success(request, 'Dziękujemy za ocenę!')
    else:
        messages.success(request, 'Twoja ocena została zaktualizowana')
    
    return redirect('event_detail', slug=slug)


@require_POST
@login_required
def delete_rating(request, slug):
    """Delete event rating"""
    event = get_object_or_404(Event, slug=slug)
    
    rating = EventRating.objects.filter(event=event, user=request.user).first()
    
    if rating:
        rating.delete()
        messages.success(request, 'Twoja ocena została usunięta')
    
    return redirect('event_detail', slug=slug)