from django.forms import ModelForm, Form, CharField

from .models import Task

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'content', 'user']

    def save(self, commit=True, delegated_by=None):
        super(TaskForm, self).save(commit=False)
        if delegated_by and self.instance.user and (delegated_by != self.instance.user):
            self.instance.delegated_by = delegated_by
        super(TaskForm, self).save(commit=commit)
