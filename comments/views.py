from django.db import models
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from comments.models import Comment
from comments.serializer import CommentSerializer
from projects.models import Project
from task.models import Task


# Create your views here.
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        task_id = self.kwargs.get('task_pk')
        if task_id:
            return Comment.objects.filter(task_id=task_id)
        return Comment.objects.filter(
            task__project__in=Project.objects.filter(
                models.Q(owner=self.request.user) |
                models.Q(members__user=self.request.user)
            ).distinct()
        )

    def perform_create(self, serializer):
        task_id = self.kwargs.get('task_pk')
        if task_id:
            task = get_object_or_404(Task, id=task_id)
            serializer.save(task=task, user=self.request.user)
        else:
            serializer.save(user=self.request.user)