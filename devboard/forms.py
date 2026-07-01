from django import forms

from devboard.models import Task, Project, Comment


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "priority", "due_date", "project", "assignee", "status", "attachment"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": "5"}),
            "project": forms.Select(attrs={"class": "form-select"}),
            "assignee": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "due_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "attachment": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
    def clean(self):
        cleaned = super().clean()
        priority = cleaned.get("priority")
        due_date = cleaned.get("due_date")
        if priority == Task.Priority.HIGH and not due_date:
            raise forms.ValidationError("Zadanie o wysokim priorytecie musi mieć określony termin wykonania")
        return cleaned
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description"]
        widgets = {"name": forms.TextInput(attrs={"class": "form-control"}), "description": forms.Textarea(attrs={"class": "form-control", "rows": "5"}),}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]