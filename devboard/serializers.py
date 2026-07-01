from rest_framework import serializers

from devboard.models import Comment, Task


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True, source="author.username")

    class Meta:
        model = Comment
        fields = ["id", "task", "author", "body", "created"]
        read_only_fields = ["author_name", "created", "id"]

class TaskSerializer(serializers.ModelSerializer):
    assignee_name = serializers.CharField(source="assignee.username", read_only=True)
    project_name = serializers.CharField(source="project.name", read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "assignee_name",
            "project",
            "project_name",
            "due_date",
            "created_at",
        ]

