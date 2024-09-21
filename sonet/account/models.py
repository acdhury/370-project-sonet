from django.db import models
from django.contrib.auth.models import User

class Bio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)



    def __str__(self):
        return f"{self.user.username}'s Bio"
