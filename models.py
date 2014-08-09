from django.db import models
from mainstay.models import UpdatedAndCreated

class Task(UpdatedAndCreated, models.Model):
    name = models.CharField(max_length=200)
    content = models.TextField()
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
