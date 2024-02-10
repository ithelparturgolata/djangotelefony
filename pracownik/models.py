from datetime import datetime
from time import timezone

from django.db import models


class Pracownik(models.Model):
	name = models.CharField(max_length=100)
	imie = models.CharField(max_length=100, default=True)
	nazwisko = models.CharField(max_length=100, default=True)
	
	def __str__(self):
		return self.imie + "  " + self.nazwisko


class Zadanie(models.Model):
	STATUS_CHOICES = (
		('in_progress', 'In Progress'),
		('completed', 'Completed')
	)
	
	description = models.TextField()
	comments = models.TextField(blank=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
	added_date = models.DateTimeField()
	deadline = models.DateField()
	assigned_to = models.ManyToManyField(Pracownik, related_name='tasks')
	task_photo = models.ImageField(upload_to='task_photos/', blank=True)
	signature_image = models.ImageField(upload_to='signature_images/', blank=True)
	# comment = models.TextField(blank=True)

	def __str__(self):
		return self.status + "  " + self.description