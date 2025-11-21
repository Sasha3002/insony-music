from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Q, Count
from django.utils import timezone
from .models import Event, EventAttendee, EventRating, EventPoll
from groups.models import Group, GroupMembership
from datetime import datetime
from django.conf import settings
import zoneinfo
from music.models import Track, PlaylistTrack, Playlist
from django.db.models import Max


@login_required
def event_list(request):
    """List all upcoming events"""
    now = timezone.now()
    
    # Get filter parameters
    filter_type = request.GET.get('filter', 'upcoming')
    city_filter = request.GET.get('city', '')
    group_slug = request.GET.get('group', '') 
    
    # Base queryset
    events = Event.objects.all()
    
    # Filter by group if specified
    if group_slug:
        group = get_object_or_404(Group, slug=group_slug)
        events = events.filter(group=group)
        # Store group for template
        filtered_group = group
    else:
        filtered_group = None
    
    # Filter by time
    if filter_type == 'past':
        events = events.filter(event_date__lt=now)
    elif filter_type == 'my':
        # Events from groups user is member of
        user_groups = Group.objects.filter(members__user=request.user, members__status='accepted')
        events = events.filter(group__in=user_groups)
    else:  # upcoming (default)
        events = events.filter(event_date__gte=now)
    
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
        'filtered_group': filtered_group,  
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
    is_attending = False
    if is_member:
        user_attendance = EventAttendee.objects.filter(
            event=event,
            user=request.user
        ).first()
        is_attending = user_attendance and user_attendance.status == 'going'
    
    # Get attendees
    attendees = event.attendees.filter(status='going').select_related('user')
    
    is_creator = event.creator == request.user
    is_admin = event.group.admin == request.user
    
    # Rating info
    user_rating = None
    can_rate = False
    
    if event.is_past and user_attendance and user_attendance.status == 'going':
        can_rate = True
        user_rating = EventRating.objects.filter(event=event, user=request.user).first()
    
    # Get all ratings
    ratings = event.ratings.select_related('user').order_by('-created_at')
    
    # Get active polls
    polls = event.polls.filter(is_active=True).select_related('creator').prefetch_related('votes')
    
    # Add user vote status and voting eligibility to each poll
    for poll in polls:
        poll.user_vote = poll.votes.filter(user=request.user).first()
        poll.can_user_vote = is_attending  # Only attendees can vote
    
    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_member': is_member,
        'is_attending': is_attending,  
        'is_creator': is_creator,
        'is_admin': is_admin,
        'user_attendance': user_attendance,
        'attendees': attendees,
        'can_rate': can_rate,
        'user_rating': user_rating,
        'ratings': ratings,
        'polls': polls,
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
        
        event_playlist = Playlist.objects.create(
            user = request.user,
            name=f"{title}",
            description=f"Playlista wydarzenia: {title}",
            is_public=True,  # Event playlists are public
            is_event_playlist=True
        )
        
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
            ,playlist=event_playlist
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


@login_required
def create_poll(request, slug):
    """Create a poll for event changes"""
    event = get_object_or_404(Event, slug=slug)

    is_attending = EventAttendee.objects.filter(
        event=event,
        user=request.user,
        status='going'
    ).exists()
    
    # Check if user is an attendee
    if not is_attending:
        messages.error(request, 'Tylko uczestnicy wydarzenia mogą tworzyć głosowania')
        return redirect('event_detail', slug=slug)
    
    # Can't create polls for past events
    if event.is_past:
        messages.error(request, 'Nie można tworzyć głosowań dla zakończonych wydarzeń')
        return redirect('event_detail', slug=slug)
    
    if request.method == 'POST':
        
        poll_type = request.POST.get('poll_type')
        title = request.POST.get('title')
        description = request.POST.get('description')
        closes_at_str = request.POST.get('closes_at')
        
        proposed_date_str = request.POST.get('proposed_date', '').strip()
        proposed_end_date_str = request.POST.get('proposed_end_date', '').strip()
        proposed_location = request.POST.get('proposed_location', '').strip()
        
        if not all([poll_type, title, description, closes_at_str]):
            messages.error(request, 'Wszystkie wymagane pola muszą być wypełnione')
            return redirect('create_poll', slug=slug)
        
        try:
            # Convert closes_at to timezone-aware
            naive_closes_at = datetime.fromisoformat(closes_at_str)
            local_tz = zoneinfo.ZoneInfo(settings.TIME_ZONE)
            closes_at = naive_closes_at.replace(tzinfo=local_tz)
            
            # Convert proposed dates if provided
            proposed_date = None
            proposed_end_date = None
            
            if proposed_date_str:
                naive_proposed_date = datetime.fromisoformat(proposed_date_str)
                proposed_date = naive_proposed_date.replace(tzinfo=local_tz)
            
            if proposed_end_date_str:
                naive_proposed_end_date = datetime.fromisoformat(proposed_end_date_str)
                proposed_end_date = naive_proposed_end_date.replace(tzinfo=local_tz)
                
        except (ValueError, Exception) as e:
            messages.error(request, f'Nieprawidłowy format daty: {e}')
            return redirect('create_poll', slug=slug)
        
        # Create poll
        poll = EventPoll.objects.create(
            event=event,
            creator=request.user,
            poll_type=poll_type,
            title=title,
            description=description,
            proposed_date=proposed_date,
            proposed_end_date=proposed_end_date,
            proposed_location=proposed_location,
            closes_at=closes_at
        )
        
        messages.success(request, 'Głosowanie zostało utworzone!')
        return redirect('event_detail', slug=slug)
    
    return render(request, 'events/poll_create.html', {
        'event': event
    })


@require_POST
@login_required
def vote_on_poll(request, poll_id):
    """Vote on a poll"""
    from .models import EventPoll, PollVote
    
    poll = get_object_or_404(EventPoll, id=poll_id)
    vote_value = request.POST.get('vote')

    attendee = EventAttendee.objects.filter(
        event=poll.event,
        user=request.user,
        status='going'
    ).first()
    
    # Check if user is a member
    if not attendee:
        messages.error(request, 'Tylko uczestnicy wydarzenia mogą głosować')
        return redirect('event_detail', slug=poll.event.slug)
    
    # Check if poll is still active
    if poll.is_closed:
        messages.error(request, 'To głosowanie zostało zakończone')
        return redirect('event_detail', slug=poll.event.slug)
    
    if vote_value not in ['yes', 'no']:
        messages.error(request, 'Nieprawidłowy głos')
        return redirect('event_detail', slug=poll.event.slug)
    
    vote_bool = vote_value == 'yes'
    
    # Create or update vote
    vote, created = PollVote.objects.update_or_create(
        poll=poll,
        user=request.user,
        defaults={'vote': vote_bool}
    )
    
    if created:
        messages.success(request, 'Twój głos został zapisany!')
    else:
        messages.success(request, 'Twój głos został zaktualizowany!')
    
    return redirect('event_detail', slug=poll.event.slug)


@require_POST
@login_required
def close_poll(request, poll_id):
    """Close a poll (creator or admin only)"""
    from .models import EventPoll
    
    poll = get_object_or_404(EventPoll, id=poll_id)
    
    # Check permissions
    if poll.creator != request.user and poll.event.group.admin != request.user:
        messages.error(request, 'Tylko twórca głosowania lub administrator może je zamknąć')
        return redirect('event_detail', slug=poll.event.slug)
    
    poll.is_active = False
    poll.save()
    
    messages.success(request, 'Głosowanie zostało zamknięte')
    return redirect('event_detail', slug=poll.event.slug)


@require_POST
@login_required
def apply_poll_changes(request, poll_id):
    """Apply poll changes to event (admin only)"""
    from .models import EventPoll
    
    poll = get_object_or_404(EventPoll, id=poll_id)
    event = poll.event
    
    # Only admin can apply changes
    if event.group.admin != request.user:
        messages.error(request, 'Tylko administrator może zastosować zmiany')
        return redirect('event_detail', slug=event.slug)
    
    # Check if poll passed (at least 50% approval)
    if poll.approval_percentage < 50:
        messages.error(request, 'Głosowanie nie uzyskało wystarczającego poparcia (wymagane minimum 50%)')
        return redirect('event_detail', slug=event.slug)
    
    # Check if there are any votes at all
    if poll.total_votes == 0:
        messages.error(request, 'Nie można zastosować zmian - brak głosów')
        return redirect('event_detail', slug=event.slug)
    
    # Apply changes based on poll type
    changes_applied = []
    
    if poll.proposed_date:
        old_date = event.event_date
        event.event_date = poll.proposed_date
        changes_applied.append(f"Data: {old_date.strftime('%d.%m.%Y %H:%M')} → {poll.proposed_date.strftime('%d.%m.%Y %H:%M')}")
    
    if poll.proposed_end_date:
        old_end = event.end_date
        event.end_date = poll.proposed_end_date
        if old_end:
            changes_applied.append(f"Koniec: {old_end.strftime('%d.%m.%Y %H:%M')} → {poll.proposed_end_date.strftime('%d.%m.%Y %H:%M')}")
        else:
            changes_applied.append(f"Koniec: {poll.proposed_end_date.strftime('%d.%m.%Y %H:%M')}")
    
    if poll.proposed_location:
        old_location = event.location
        event.location = poll.proposed_location
        changes_applied.append(f"Miejsce: {old_location} → {poll.proposed_location}")
    
    if changes_applied:
        event.save()
        
        # Close the poll after applying
        poll.is_active = False
        poll.save()
        
        # Create a success message with details
        changes_text = "<br>".join(changes_applied)
        messages.success(request, f'Zmiany zostały zastosowane!<br>{changes_text}')
    else:
        messages.warning(request, 'Brak zmian do zastosowania')
    
    return redirect('event_detail', slug=event.slug)



@login_required
def event_playlist_add_track(request, slug):
    """Add track to event playlist (creator only)"""
    from music.models import Track, PlaylistTrack

    event = get_object_or_404(Event, slug=slug)
    
    # Only creator can add tracks
    if event.creator != request.user:
        messages.error(request, 'Tylko twórca wydarzenia może dodawać utwory do playlisty')
        return redirect('event_detail', slug=slug)
    
    if not event.playlist:
        messages.error(request, 'To wydarzenie nie ma playlisty')
        return redirect('event_detail', slug=slug)
    
    if request.method == 'POST':
        
        track_id = request.POST.get('track_id')
        track = get_object_or_404(Track, id=track_id)
        
        # Check if track already in playlist
        if PlaylistTrack.objects.filter(playlist=event.playlist, track=track).exists():
            messages.warning(request, f'Utwór "{track.title}" już jest w playliście')
            return redirect('event_playlist_add_track', slug=slug)
        
        # Get next position
        max_position = PlaylistTrack.objects.filter(playlist=event.playlist).aggregate(Max('position'))['position__max'] or 0
        
        # Add track to playlist
        PlaylistTrack.objects.create(
            playlist=event.playlist,
            track=track,
            position=max_position + 1
        )
        
        messages.success(request, f'Dodano "{track.title}" do playlisty wydarzenia')
        return redirect('event_detail', slug=slug)
    
    # GET request - show track search
    
    query = request.GET.get('q', '')
    if query:
        tracks = Track.objects.filter(
            Q(title__icontains=query) | 
            Q(artist__name__icontains=query)  # Fix: use artist__name
        ).select_related('artist')[:20]
    else:
        tracks = Track.objects.all().select_related('artist')[:20]
    
    return render(request, 'events/event_playlist_add.html', {
        'event': event,
        'tracks': tracks,
        'query': query,
    })


@require_POST
@login_required
def event_playlist_remove_track(request, slug, track_id):
    """Remove track from event playlist (creator only)"""
    event = get_object_or_404(Event, slug=slug)
    
    # Only creator can remove tracks
    if event.creator != request.user:
        messages.error(request, 'Tylko twórca wydarzenia może usuwać utwory z playlisty')
        return redirect('event_detail', slug=slug)
    
    if not event.playlist:
        messages.error(request, 'To wydarzenie nie ma playlisty')
        return redirect('event_detail', slug=slug)
    
    from music.models import PlaylistTrack
    
    playlist_track = get_object_or_404(
        PlaylistTrack, 
        playlist=event.playlist, 
        track_id=track_id
    )
    
    track_title = playlist_track.track.title
    playlist_track.delete()
    
    messages.success(request, f'Usunięto "{track_title}" z playlisty')
    return redirect('event_detail', slug=slug)