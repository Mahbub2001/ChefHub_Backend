from django.contrib import admin
from django.urls import path, include
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from recipe.views import PublicRecipeListAPIView
from event.views import PublicEventListAPIView
from chef import views

class CustomAPIRoot(APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            'register': reverse('register', request=request),
            'login': reverse('login', request=request),
            'logout': reverse('logout', request=request),
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
    # Define the empty path to point to the custom API root view
    path('', CustomAPIRoot.as_view(), name='api-root'),
]

