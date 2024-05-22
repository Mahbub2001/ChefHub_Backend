from django.db import models
from chef.models import Chef 

class Event(models.Model):
    event_name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(Chef, related_name='events', on_delete=models.CASCADE)

    def __str__(self):
        return self.event_name
