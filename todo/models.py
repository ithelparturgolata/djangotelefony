from datetime import datetime
from time import timezone

from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)

class Task(models.Model):
    STATUS_CHOICES = (
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    )

    description = models.TextField()
    comments = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    added_date = models.DateTimeField(default=True)
    deadline = models.DateField()
    assigned_to = models.ManyToManyField(Employee, related_name='tasks')
    task_photo = models.ImageField(upload_to='task_photos/', blank=True)
    signature_image = models.ImageField(upload_to='signature_images/', blank=True)
    # comment = models.TextField(blank=True)