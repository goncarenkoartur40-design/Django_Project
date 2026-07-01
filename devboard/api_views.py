from rest_framework import viewsets, permissions
from devboard.serializers import CommentSerializer, TaskSerializer
from devboard.models import Comment, Task
from devboard.serializers import TaskSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user).select_related("author", "task")
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.filter(
            project__owner=self.request.user
        ).select_related("project", "assignee")

        status = self.request.query_params.get("status")
        priority = self.request.query_params.get("priority")
        project = self.request.query_params.get("project")
        title = self.request.query_params.get("title")
        due_date = self.request.query_params.get("due_date")
        assignee = self.request.query_params.get("assignee")
        ordering = self.request.query_params.get("ordering")
        due_date_from = self.request.query_params.get("due_date_from")
        due_date_to = self.request.query_params.get("due_date_to")
        has_due_date = self.request.query_params.get("has_due_date")
        created_from = self.request.query_params.get("created_from")
        created_to = self.request.query_params.get("created_to")
        description = self.request.query_params.get("description")

        if status:
            queryset = queryset.filter(status=status)

        if priority:
            queryset = queryset.filter(priority=priority)

        if project:
            queryset = queryset.filter(project=project)

        if title:
            queryset = queryset.filter(title__icontains=title)

        if due_date:
            queryset = queryset.filter(due_date=due_date)

        if assignee:
            queryset = queryset.filter(assignee=assignee)

        if due_date_from:
            queryset = queryset.filter(due_date__gte=due_date_from)

        if due_date_to:
            queryset = queryset.filter(due_date__lte=due_date_to)

        if has_due_date == "true":
            queryset = queryset.filter(due_date__isnull=False)

        if has_due_date == "false":
            queryset = queryset.filter(due_date__isnull=True)

        if created_from:
            queryset = queryset.filter(created_at__date__gte=created_from)

        if created_to:
            queryset = queryset.filter(created_at__date__lte=created_to)

        if description:
            queryset = queryset.filter(description__icontains=description)

        allowed_ordering = [
            "title",
            "-title",
            "priority",
            "-priority",
            "created_at",
            "-created_at",
            "due_date",
            "-due_date",
        ]

        if ordering in allowed_ordering:
            queryset = queryset.order_by(ordering)

        return queryset