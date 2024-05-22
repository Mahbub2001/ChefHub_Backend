from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Recipe
from .serializers import RecipeSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from chef.models import Chef
from rest_framework.authentication import TokenAuthentication

class RecipeViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

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
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)    

    def perform_create(self, serializer):
        serializer.save(chef=self.request.user)

class PublicRecipeListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
