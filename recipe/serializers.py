from rest_framework import serializers
from .models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'ingredients', 'instructions', 'creation_date', 'image_url', 'chef']
        # read_only_fields = ['creation_date', 'chef']
