from django.db import models
from mainstay.models import UpdatedAndCreated


class TaskUsersManager(models.Manager):
    def for_user(self, user):
        return self.get_queryset().filter(models.Q(user=user) | models.Q(user=None))


class Task(UpdatedAndCreated, models.Model):
    name = models.CharField(max_length=200)
    content = models.TextField()
    user = models.ForeignKey('auth.User', blank=True, null=True)
    delegated_by = models.ForeignKey('auth.User', blank=True, null=True, related_name='delegated_tasks')
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    objects = TaskUsersManager()
