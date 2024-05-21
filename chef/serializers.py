from rest_framework import serializers
from .models import Chef
from django.contrib.auth.models import User
from recipe.models import Recipe

class ChefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chef
        fields = ['id', 'user', 'bio', 'profile_picture','phone_number', 'home','gender']

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'ingredients', 'instructions', 'creation_date', 'image_url']

class ChefSerializer(serializers.ModelSerializer):
    recipes = RecipeSerializer(many=True, read_only=True) 

    class Meta:
        model = Chef
        fields = ['id', 'user', 'bio', 'profile_picture','phone_number', 'home', 'gender', 'recipes'] 

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required = True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
    
    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']
        
        if password != password2:
            raise serializers.ValidationError({'error' : "Password Doesn't Mactched"})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error' : "Email Already exists"})
        account = User(username = username, email=email, first_name = first_name, last_name = last_name)
        print(account)
        account.set_password(password)
        account.is_active = False
        account.save()
        Chef.objects.create(user=account)
        return account


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)