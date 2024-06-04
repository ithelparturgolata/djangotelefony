from django.db import models
from django.utils import timezone


class Contractor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    
class Department(models.Model):
    department_name = models.CharField(max_length=100)

    def __str__(self):
        return self.department_name


class Contract(models.Model):
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    indefinite = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, default='Aktywna')
    place = models.CharField(max_length=20, blank=True, null=True)
    
    def is_expired(self):
        if self.end_date is None:
            self.status = 'Aktywna'
            self.save()
            return
        
        days_left = (self.end_date - timezone.now().date()).days
        
        if days_left <= 0:
            self.status = 'Wygasła'
        elif days_left <= 45:
            self.status = 'Poniżej 45 dni do końca'
        else:
            self.status = 'Aktywna'
        
        self.save()
    

class ContractFile(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    file = models.FileField(upload_to='contract_files/')

    def __str__(self):
        return self.file.name
    
    
class ContractFileAnnex(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    file_annex = models.FileField(upload_to='contract_files/')

    def __str__(self):
        return self.file_annex.name

    