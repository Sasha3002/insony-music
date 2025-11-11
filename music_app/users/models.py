from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Lower
from django.core.validators import MinValueValidator

class User(AbstractUser):
    email = models.EmailField(unique=True)  
    favorite_genres = models.TextField(blank=True, default="")
    favorite_artists = models.TextField(blank=True, default="")
    bio = models.TextField(blank=True, default="")
    xp = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True, null=True)
    email_verification_sent_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('email'),
                name='users_user_email_ci_unique'
            )
        ]
    @property
    def level(self):
        return self.xp // 1000

    @property
    def level_progress(self):
        return self.xp % 1000
    

class UserFollow(models.Model):
    """User following/subscription system"""
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'following')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.follower.username} → {self.following.username}"


class UserBlock(models.Model):
    """User blocking system"""
    blocker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blocking'
    )
    blocked = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blocked_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('blocker', 'blocked')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.blocker.username} ✕ {self.blocked.username}"
    

class ErrorReport(models.Model):
    """User error reports - general and content-specific"""
    STATUS_CHOICES = [
        ('pending', 'Oczekujący'),
        ('in_progress', 'W trakcie'),
        ('resolved', 'Rozwiązany'),
    ]
    
    CONTENT_TYPE_CHOICES = [
        ('general', 'Ogólny problem'),
        ('review', 'Nieodpowiednia recenzja'),
        ('profile', 'Nieodpowiedni profil'),
        ('playlist', 'Nieodpowiednia playlista'),
        ('track', 'Nieodpowiedni utwór'),
    ]
    
    REASON_CHOICES = [
        ('spam', 'Spam'),
        ('inappropriate', 'Treść nieodpowiednia'),
        ('harassment', 'Molestowanie/Nękanie'),
        ('hate_speech', 'Mowa nienawiści'),
        ('fake', 'Fałszywe informacje'),
        ('copyright', 'Naruszenie praw autorskich'),
        ('violence', 'Treści przemocy'),
        ('other', 'Inne'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='error_reports'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    page_url = models.CharField(max_length=500, blank=True)
    

    content_type = models.CharField(
        max_length=50, 
        choices=CONTENT_TYPE_CHOICES,
        default='general'
    )
    content_id = models.PositiveIntegerField(null=True, blank=True)
    report_reason = models.CharField(
        max_length=50,
        choices=REASON_CHOICES,
        blank=True
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_reports'
    )
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        if self.content_type == 'general':
            return f"{self.user.username} - {self.title} [{self.status}]"
        else:
            return f"{self.user.username} - {self.get_content_type_display()} #{self.content_id} [{self.status}]"
    
    def get_content_object(self):
        """Get the reported content object"""
        if self.content_type == 'review' and self.content_id:
            from music.models import Review
            try:
                return Review.objects.get(id=self.content_id)
            except Review.DoesNotExist:
                return None
        elif self.content_type == 'profile' and self.content_id:
            try:
                return User.objects.get(id=self.content_id)
            except User.DoesNotExist:
                return None
        # Add more content types as needed
        return None