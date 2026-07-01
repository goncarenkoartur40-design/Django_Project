from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from devboard.forms import TaskForm, ProjectForm, CommentForm
from devboard.models import Project, Task, Comment
from rest_framework import viewsets
from .serializers import TaskSerializer

# def index(request):
#     return HttpResponse("<h1>DevBoard - etap 1: scaffold!</h1>")
# def index(request):
#     return render(request, "index.html")
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "devboard/project_list.html"
    context_object_name = "projects"
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get("q")
        sort = self.request.GET.get("sort")
        projects = (
            Project.objects.filter(owner=self.request.user)
            .annotate(task_count=Count("tasks"))
            .order_by("-created_at")
        )
        if query:
            projects = projects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        if sort =="old":
            projects = projects.order_by("created_at")
        elif sort == "name":
            projects = projects.order_by("name")
        elif sort == "-name":
            projects = projects.order_by("-name")
        else:
            projects = projects.order_by("-created_at")

        return projects
class ProjectDetailView(DetailView, LoginRequiredMixin):
    model = Project
    template_name = "devboard/project_detail.html"
    context_object_name = "project"
    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        tasks = (
            self.object.tasks
            .select_related("assignee")
            .order_by("priority", "due_date")
        )
        status = self.request.GET.get("status")
        if status:
            tasks = tasks.filter(status=status)
        ctx["tasks"] = tasks
        ctx["comment_form"] = CommentForm()

        return ctx
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        task_id = self.kwargs["task_pk"]
        task = Task.objects.get(pk=task_id)
        form.instance.task = task
        form.instance.author = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy("devboard:project-detail", kwargs={"pk": self.object.task.project.pk},)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "devboard/project_create.html"
    def get_success_url(self):
        return reverse_lazy("devboard:project-detail", kwargs={"pk": self.object.pk},)

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)
class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = "devboard/project_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("devboard:lista-project")

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "devboard/project_create.html"
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy("devboard:lista-project")
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "devboard/task_create.html"
    def get_success_url(self):
        return reverse_lazy("devboard:project-detail",kwargs={"pk":self.object.project.pk})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["project"].queryset = Project.objects.filter(owner=self.request.user)
        return form

    def form_valid(self, form):
        messages.success(self.request, f"Zadanie '{form.instance.title}' zostało dodane.")
        return super().form_valid(form)
    def get_initial(self):
        initial = super().get_initial()
        project_id = self.request.GET.get("project")
        if project_id:
            initial["project"] = project_id
            return initial

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "devboard/task_create.html"
    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy("devboard:project-detail", kwargs={"pk": self.object.project.pk})

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "devboard/task_confirm_delete.html"
    def get_success_url(self):
        return reverse_lazy("devboard:project-detail",kwargs={"pk": self.object.project.pk})
    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer