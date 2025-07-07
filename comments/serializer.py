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

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)