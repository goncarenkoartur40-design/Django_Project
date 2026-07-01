from django.urls import path
from devboard import views
from devboard.views import ProjectDetailView, ProjectUpdateView, TaskCreateView, TaskUpdateView, TaskDeleteView, \
    ProjectDeleteView, ProjectCreateView, CommentCreateView, TaskViewSet
from devboard import views
from rest_framework.routers import DefaultRouter
app_name = "devboard"
router = DefaultRouter()
router.register("api/tasks", views.TaskViewSet, basename="api-tasks")

urlpatterns = [

    path("", views.ProjectListView.as_view(), name="lista-project"),
    path("project/<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path("project/<int:pk>/edytuj/", ProjectUpdateView.as_view(), name="project-edit"),
    path("zadania/nowe/", views.TaskCreateView.as_view(), name="task-create"),
    path("zadania/<int:pk>/edytuj/", TaskUpdateView.as_view(), name="task-edit"),
    path("zadania/<int:pk>/usun/", TaskDeleteView.as_view(), name="task-delete"),
    path("project/<int:pk>/usun/",ProjectDeleteView.as_view(), name="project-delete"),
    path("project/nowy/", ProjectCreateView.as_view(), name="project-create"),
    path("zadania/<int:task_pk>/komentarz/", CommentCreateView.as_view(), name="comment-create"),
]
urlpatterns += router.urls