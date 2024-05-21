from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Recipe
from .serializers import RecipeSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from chef.models import Chef

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.query_params.get('title')
        chef_id = self.request.query_params.get('chef_id')
        if title:
            queryset = queryset.filter(title__icontains=title)
        if chef_id:
            try:
                chef = Chef.objects.get(id=chef_id)
                queryset = queryset.filter(chef=chef)
            except Chef.DoesNotExist:
                queryset = Recipe.objects.none()

        return queryset

    def perform_create(self, serializer):
        serializer.save(chef=self.request.user)

class PublicRecipeListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
