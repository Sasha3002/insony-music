from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from groups.models import Group
from django.utils import timezone
from music.models import Playlist

User = get_user_model()

class Event(models.Model):
    """Music event organized by a group"""
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='events')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    
    # Event details
    location = models.CharField(max_length=200, help_text="Dokładne miejsce (np. nazwa klubu, ulica)")
    event_date = models.DateTimeField(help_text="Data i godzina rozpoczęcia")
    end_date = models.DateTimeField(help_text="Data i godzina zakończenia", blank=True, null=True)
    
    # Optional image
    event_image = models.ImageField(upload_to='event_images/', blank=True, null=True)

    # Event playlist
    playlist = models.ForeignKey(Playlist, on_delete=models.SET_NULL, null=True, blank=True, related_name='event')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['event_date']
    
    def __str__(self):
        return f"{self.title} - {self.group.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Event.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    @property
    def is_past(self):
        end_time = self.end_date if self.end_date else self.event_date
        return end_time < timezone.now()
    
    @property
    def attendee_count(self):
        return self.attendees.filter(status='going').count()
    
    @property
    def city(self):
        """Get city from group location"""
        return self.group.location
    
    @property
    def full_location(self):
        """Get full location: venue in city"""
        return f"{self.location}, {self.group.location}"
    
    @property
    def average_rating(self):
        """Calculate average rating"""
        ratings = self.ratings.all()
        if not ratings:
            return 0
        return sum(r.rating for r in ratings) / len(ratings)

    @property
    def rating_count(self):
        """Get total number of ratings"""
        return self.ratings.count()

    def get_user_rating(self, user):
        """Get rating by specific user"""
        return self.ratings.filter(user=user).first()


class EventAttendee(models.Model):
    """Track who's attending events"""
    STATUS_CHOICES = [
        ('going', 'Idę'),
        ('maybe', 'Może'),
        ('not_going', 'Nie idę'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendees')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='going')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('event', 'user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.status})"
    
class EventRating(models.Model):
    """User ratings for past events"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('event', 'user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.event.title}: {self.rating}★"
    

class EventPoll(models.Model):
    """Poll for event changes"""
    POLL_TYPES = [
        ('time', 'Zmiana czasu'),
        ('location', 'Zmiana miejsca'),
        ('date', 'Zmiana daty'),
        ('other', 'Inne'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='polls')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_polls')
    
    poll_type = models.CharField(max_length=20, choices=POLL_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Proposed changes
    proposed_date = models.DateTimeField(blank=True, null=True, help_text="Proponowana nowa data rozpoczęcia")
    proposed_end_date = models.DateTimeField(blank=True, null=True, help_text="Proponowana nowa data zakończenia")
    proposed_location = models.CharField(max_length=200, blank=True, help_text="Proponowane nowe miejsce")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    closes_at = models.DateTimeField(help_text="Kiedy głosowanie się kończy")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.event.title}"
    
    @property
    def is_closed(self):
        return timezone.now() > self.closes_at or not self.is_active
    
    @property
    def votes_for(self):
        return self.votes.filter(vote=True).count()
    
    @property
    def votes_against(self):
        return self.votes.filter(vote=False).count()
    
    @property
    def total_votes(self):
        return self.votes.count()
    
    @property
    def approval_percentage(self):
        total = self.total_votes
        if total == 0:
            return 0
        return (self.votes_for / total) * 100


class PollVote(models.Model):
    """Individual vote on a poll"""
    poll = models.ForeignKey(EventPoll, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.BooleanField(help_text="True = Za, False = Przeciw")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('poll', 'user')
        ordering = ['-created_at']
    
    def __str__(self):
        vote_text = "Za" if self.vote else "Przeciw"
        return f"{self.user.username} - {vote_text}"