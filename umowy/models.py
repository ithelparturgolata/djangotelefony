from django.db import models
from django.utils import timezone


class Contractor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Contract(models.Model):
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=100, default='Aktywna')
    
    def is_expired(self):
        # Calculate the number of days left until the end of the contract
        days_left = (self.end_date - timezone.now().date()).days

        # Update status based on the number of days left
        if days_left <= 0:
            self.status = 'Wygasła'
        elif days_left <= 45:
            self.status = 'Poniżej 45 dni do końca'
        else:
            self.status = 'Aktywna'
    
        self.save()
    
    def status_css_class(self):
        if self.status == 'Wygasła':
            return 'btn btn-danger'
        elif self.status == 'Poniżej 45 dni do końca':
            return 'btn btn-warning'
        else:
            return 'btn btn-success'
    

class ContractFile(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    file = models.FileField(upload_to='contract_files/')

    def __str__(self):
            return self.file.name
    
    
    
    
    
    
    