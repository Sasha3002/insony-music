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