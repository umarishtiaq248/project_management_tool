from django.contrib.auth.models import User
from django.db import models
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from projects.models import Project, ProjectMember
from projects.serializers import ProjectSerializer
from task.models import Task
from task.serializers import TaskSerializer


# Create your views here.
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only see projects they own or are members of
        return Project.objects.filter(
            models.Q(owner=self.request.user) |
            models.Q(members__user=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)
        # Add owner as admin member
        ProjectMember.objects.create(
            project=project,
            user=self.request.user,
            role='Admin'
        )

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        project = self.get_object()

        # Check if user is admin of the project
        try:
            member = ProjectMember.objects.get(project=project, user=request.user)
            if member.role != 'Admin':
                return Response({'error': 'Only project admins can add members'}, status=403)
        except ProjectMember.DoesNotExist:
            return Response({'error': 'You are not a member of this project'}, status=403)

        user_id = request.data.get('user_id')
        role = request.data.get('role', 'Member')

        if not user_id:
            return Response({'error': 'user_id is required'}, status=400)

        # Validate role
        if role not in ['Admin', 'Member']:
            return Response({'error': 'Invalid role. Must be Admin or Member'}, status=400)

        try:
            user = User.objects.get(id=user_id)
            member, created = ProjectMember.objects.get_or_create(
                project=project,
                user=user,
                defaults={'role': role}
            )

            if not created:
                return Response({'error': 'User is already a member'}, status=400)

            return Response({'message': 'Member added successfully'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None):
        project = self.get_object()
        tasks = Task.objects.filter(project=project)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
