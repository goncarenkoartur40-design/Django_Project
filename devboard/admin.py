from django.contrib import admin

from .models import Project, Task, Comment

admin.site.register(Comment)

class TaskInline(admin.TabularInline):
    """Zadania wyświetlane wewnątrz projektu."""
    model = Task
    fields = ("title", "status", "priority", "assignee", "due_date")
    extra = 1
    show_change_link = True

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id","name", "owner", "name", "created_at")
    search_fields = ("name",)
    list_filter = ("name",)
search_fields = ("name","description")
list_filter = ("name", "created_at")
inlines = [TaskInline]



@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "project", "status", "priority", "created_at",)
    search_fields = ("title", "description")
    list_filter = ("status", "priority")

admin.site.site_header = "DevBoard - Panel Administracyjny"
admin.site.site_title = "DevBoard Admin"
admin.site.index_title = "Zadanie Admin"

