
from django.db import models
from django.contrib.auth.models import User


class Events(models.Model):
    created_by = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.TextField(blank=False)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title

