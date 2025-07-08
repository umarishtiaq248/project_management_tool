from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from task.views import TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
urlpatterns = [
    path('', include(router.urls)),
    path('projects/<int:project_pk>/tasks/', TaskViewSet.as_view({'get': 'list', 'post': 'create'}), name='project-tasks'),
]
