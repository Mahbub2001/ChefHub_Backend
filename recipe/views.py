from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Recipe
from .serializers import RecipeSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(chef=self.request.user.chef)



class PublicRecipeListAPIView(generics.ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [AllowAny]
