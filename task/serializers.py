from django.contrib.auth.models import User
from rest_framework import serializers

from project_management_tool.serializers import UserSerializer
from projects.serializers import ProjectSerializer
from task.models import Task


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    assigned_to_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'assigned_to',
                  'assigned_to_id', 'project', 'created_at', 'due_date']
        read_only_fields = ['id', 'created_at']

    def validate_assigned_to_id(self, value):
        if value:
            try:
                user = User.objects.get(id=value)
                return value
            except User.DoesNotExist:
                raise serializers.ValidationError('User not found')
        return value

    def validate_due_date(self, value):
        if value:
            from django.utils import timezone
            if value < timezone.now():
                raise serializers.ValidationError('Due date cannot be in the past')
        return value

    def validate(self, attrs):
        # Validate assigned user is a member of the project
        assigned_to_id = attrs.get('assigned_to_id')
        project = attrs.get('project') or (hasattr(self, 'instance') and self.instance and self.instance.project)

        if assigned_to_id and project:
            from projects.models import ProjectMember
            try:
                user = User.objects.get(id=assigned_to_id)
                if not ProjectMember.objects.filter(project=project, user=user).exists():
                    raise serializers.ValidationError({
                        'assigned_to_id': 'User must be a member of the project'
                    })
            except User.DoesNotExist:
                raise serializers.ValidationError({'assigned_to_id': 'User not found'})

        return attrs

    def create(self, validated_data):
        assigned_to_id = validated_data.pop('assigned_to_id', None)
        if assigned_to_id:
            validated_data['assigned_to'] = User.objects.get(id=assigned_to_id)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        assigned_to_id = validated_data.pop('assigned_to_id', None)
        if assigned_to_id is not None:
            if assigned_to_id:
                validated_data['assigned_to'] = User.objects.get(id=assigned_to_id)
            else:
                validated_data['assigned_to'] = None
        return super().update(instance, validated_data)
