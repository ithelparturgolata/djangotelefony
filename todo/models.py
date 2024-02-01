from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=20)
    comments = models.TextField(blank=True)
    date_added = models.DateField()
    due_date = models.DateField()
    administracja = models.CharField(max_length=2, default=True)