from rest_framework import serializers

from project_management_tool.serializers import UserSerializer
from projects.models import ProjectMember, Project


class ProjectMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ProjectMember
        fields = ['id', 'user', 'role']


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    members = ProjectMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'created_at', 'members']
        read_only_fields = ['id', 'created_at']

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('Project name cannot be empty')
        if len(value) > 255:
            raise serializers.ValidationError('Project name cannot exceed 255 characters')
        return value.strip()

    def validate_description(self, value):
        if value and len(value) > 1000:
            raise serializers.ValidationError('Project description cannot exceed 1000 characters')
        return value
