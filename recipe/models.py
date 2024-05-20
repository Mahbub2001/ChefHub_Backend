from django.db import models
from chef.models import Chef  

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(null=True, blank=True)
    chef = models.ForeignKey(Chef, related_name='recipes', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
