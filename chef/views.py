from .models import Chef
from .serializers import ChefSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from . import serializers
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework.authtoken.models import Token
from django.core.mail import EmailMultiAlternatives
from rest_framework.permissions import AllowAny
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout


class ChefViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Chef.objects.all()
    serializer_class = ChefSerializer

class ChefProfileViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        user_id = request.query_params.get('user')
        if user_id is None:
            return Response({"error": "User ID is required in the query parameters."}, status=400)

        try:
            chef = Chef.objects.get(id=user_id)  
            serializer = ChefSerializer(chef)
            return Response(serializer.data)
        except Chef.DoesNotExist:
            return Response({"error": "Chef profile not found for the provided user ID."}, status=404)

    def update(self, request, pk=None):
        try:
            chef = Chef.objects.get(pk=pk)
        except Chef.DoesNotExist:
            return Response({"error": "Chef profile not found."}, status=404)

        serializer = ChefSerializer(chef, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class UserRegistrationApiView(APIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            # confirm_link = f"http://127.0.0.1:8000/chef/active/{uid}/{token}"
            confirm_link = f"https://chefhub-backend.onrender.com/chef/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})

            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response("Check your mail for confirmation")
        return Response(serializer.errors)

def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = Chef._default_manager.get(pk=uid)
    except (Chef.DoesNotExist):
        user = None 

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')

class UserLoginApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=self.request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(email=email, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({'token': token.key, 'user_id': user.id})
            else:
                return Response({'error': "Invalid Credential"})
        return Response(serializer.errors)

class UserLogoutView(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')
