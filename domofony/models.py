from django.db import models


class EstateIntercom(models.TextChoices):
    NW = 'NW', 'Na Wyżynach'
    NS = 'NS', 'Na Skarpie'
    CE = 'CE', 'Centrum'


class ContractorIntercom(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    login = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} {self.surname}"


class TaskIntercom(models.Model):
    user = models.CharField(max_length=100)
    description = models.TextField()
    estate = models.CharField(max_length=2, choices=EstateIntercom.choices)
    street = models.CharField(max_length=100)
    contractor = models.ForeignKey(ContractorIntercom, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=(('completed', 'Completed'), ('in_progress', 'In Progress')))
    added_date = models.DateField(auto_now_add=True)
    planned_execution_date = models.DateField()
    actual_execution_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.description
