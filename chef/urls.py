from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'chefs', views.ChefViewSet)
router.register(r'profile', views.ChefProfileViewSet, basename='chef-profile')

urlpatterns = [
    path('', include(router.urls)),
    path('active/<uid64>/<token>/', views.activate, name='activate'),
]
