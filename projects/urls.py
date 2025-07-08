from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from projects.views import ProjectViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
urlpatterns = [
    path('', include(router.urls)),
]
