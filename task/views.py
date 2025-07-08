from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from comments.models import Comment
from comments.serializers import CommentSerializer
from projects.models import Project
from task.models import Task
from task.serializers import TaskSerializer


# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs.get('project_pk')
        if project_id:
            # Ensure user has access to the project
            try:
                project = Project.objects.get(
                    models.Q(id=project_id) &
                    (models.Q(owner=self.request.user) |
                     models.Q(members__user=self.request.user))
                )
                return Task.objects.filter(project=project)
            except Project.DoesNotExist:
                return Task.objects.none()
        return Task.objects.filter(
            project__in=Project.objects.filter(
                models.Q(owner=self.request.user) |
                models.Q(members__user=self.request.user)
            ).distinct()
        )

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_pk')
        if project_id:
            # Ensure user has access to the project
            project = get_object_or_404(
                Project.objects.filter(
                    models.Q(id=project_id) &
                    (models.Q(owner=self.request.user) |
                     models.Q(members__user=self.request.user))
                )
            )
            serializer.save(project=project)
        else:
            serializer.save()

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        task = self.get_object()
        comments = Comment.objects.filter(task=task)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
