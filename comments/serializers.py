from rest_framework import serializers

from comments.models import Comment
from project_management_tool.serializers import UserSerializer
from task.serializers import TaskSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    task = TaskSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'task', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_content(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('Comment content cannot be empty')
        if len(value) > 1000:
            raise serializers.ValidationError('Comment content cannot exceed 1000 characters')
        return value.strip()

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
