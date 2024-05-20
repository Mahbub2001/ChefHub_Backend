from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import EventViewSet

router = DefaultRouter()
router.register('events', EventViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
