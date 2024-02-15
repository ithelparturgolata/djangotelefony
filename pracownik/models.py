from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = (
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    description = models.TextField()
    added_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    photo = models.ImageField(upload_to='task_photos/', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')

class TaskAssignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)

class TaskComment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class TaskPhoto(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='additional_photos')
    image = models.ImageField(upload_to='additional_task_photos/', blank=True)
