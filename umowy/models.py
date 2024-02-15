from django.db import models

class Contractor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Contract(models.Model):
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    file = models.FileField(upload_to='contracts/')
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    def is_expired(self):
        from django.utils import timezone
        return self.end_date < timezone.now().date()
