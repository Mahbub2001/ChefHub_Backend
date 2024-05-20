from django.contrib import admin
from django.urls import path, include
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from recipe.views import PublicRecipeListAPIView
from event.views import PublicEventListAPIView
from rest_framework.permissions import AllowAny
from chef import views

class CustomAPIRoot(APIView):
    permission_classes = [AllowAny] 
    def get(self, request, *args, **kwargs):
        return Response({
            'recipelist': reverse('public-recipe-list', request=request),
            'eventlist': reverse('public-event-list', request=request),
        })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chef/', include('chef.urls')),
    path('recipe/', include('recipe.urls')),
    path('event/', include('event.urls')),
    path('register/', views.UserRegistrationApiView.as_view(), name='register'),
    path('login/', views.UserLoginApiView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('recipelist/', PublicRecipeListAPIView.as_view(), name='public-recipe-list'),
    path('eventlist/', PublicEventListAPIView.as_view(), name='public-event-list'),
    path('', CustomAPIRoot.as_view(), name='api-root'),
]

