from rest_framework import serializers
from .models import Chef
from recipe.models import Recipe

class ChefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chef
        fields = ['id', 'email', 'username', 'bio', 'profile_picture', 'phone_number', 'home', 'gender']

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'ingredients', 'instructions', 'creation_date', 'image_url']

class ChefSerializer(serializers.ModelSerializer):
    recipes = RecipeSerializer(many=True, read_only=True)
    class Meta:
        model = Chef
        fields = ['id', 'email', 'username', 'bio', 'profile_picture', 'phone_number', 'home', 'gender', 'recipes']

from rest_framework import serializers
from .models import Chef

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)
    
    class Meta:
        model = Chef
        fields = ['username', 'email', 'password', 'confirm_password', 'bio', 'profile_picture', 'phone_number', 'home', 'gender']

    def save(self):
        email = self.validated_data['email']
        username = self.validated_data['username']
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']
        bio = self.validated_data.get('bio', '')
        profile_picture = self.validated_data.get('profile_picture', '')
        phone_number = self.validated_data.get('phone_number', '')
        home = self.validated_data.get('home', '')
        gender = self.validated_data.get('gender', '')

        if password != password2:
            raise serializers.ValidationError({'error': "Passwords do not match"})
        if Chef.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': "Email already exists"})

        account = Chef(
            email=email,
            username=username,
            bio=bio,
            profile_picture=profile_picture,
            phone_number=phone_number,
            home=home,
            gender=gender
        )
        account.set_password(password)
        account.is_active = False
        account.save()
        return account

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
