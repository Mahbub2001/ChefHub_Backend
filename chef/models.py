from django.db import models
from django.contrib.auth.models import User 

class Chef(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_picture = models.URLField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    home = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other')), null=True, blank=True)

    def __str__(self):
        return self.user.username
