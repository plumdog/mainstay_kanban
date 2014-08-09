from django.forms import ModelForm, Form, CharField

from .models import Task

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'content']
