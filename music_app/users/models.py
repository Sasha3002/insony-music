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