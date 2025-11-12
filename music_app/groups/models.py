from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from music.models import Genre

User = get_user_model()

class Group(models.Model):
    """Music group for organizing events"""
    TYPE_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    location = models.CharField(max_length=200, help_text="City or place where group is based")
    
    # Visual
    cover_image = models.ImageField(upload_to='group_covers/', blank=True, null=True)
    
    # Type
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='public')
    
    # Admin/Creator
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='administered_groups')
    
    # Genres (store as comma-separated for simple filtering)
    genres = models.ManyToManyField(Genre, blank=True, related_name='groups')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def member_count(self):
        return self.members.filter(status='accepted').count()
    
    @property
    def genres_list(self):
        """Return genres as a list"""
        if self.genres:
            return [g.strip() for g in self.genres.split(',')]
        return []


class GroupMembership(models.Model):
    """Track group memberships"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),      # For private groups
        ('accepted', 'Accepted'),    # Active member
        ('rejected', 'Rejected'),    # Request denied
    ]
    
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_memberships')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='accepted')
    
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('group', 'user')
        ordering = ['-joined_at']
    
    def __str__(self):
        return f"{self.user.username} in {self.group.name} ({self.status})"


class GroupInvitation(models.Model):
    """Invitations to join groups"""
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='invitations')
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    invited_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations')
    
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('group', 'invited_user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Invitation: {self.invited_user.username} → {self.group.name}"