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

    def create(self, validated_data):
        assigned_to_id = validated_data.pop('assigned_to_id', None)
        if assigned_to_id:
            try:
                validated_data['assigned_to'] = User.objects.get(id=assigned_to_id)
            except User.DoesNotExist:
                raise serializers.ValidationError({'assigned_to_id': 'User not found'})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        assigned_to_id = validated_data.pop('assigned_to_id', None)
        if assigned_to_id is not None:
            if assigned_to_id:
                try:
                    validated_data['assigned_to'] = User.objects.get(id=assigned_to_id)
                except User.DoesNotExist:
                    raise serializers.ValidationError({'assigned_to_id': 'User not found'})
            else:
                validated_data['assigned_to'] = None
        return super().update(instance, validated_data)