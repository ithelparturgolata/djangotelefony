from django.db import models


class UsersIT(models.Model):
	name = models.CharField(max_length=100, null=True, blank=True)
	surname = models.CharField(max_length=100, null=True, blank=True)
	administration = models.CharField(max_length=3, null=True, blank=True)
	address_ip_pc = models.CharField(max_length=20, null=True, blank=True)
	login = models.CharField(max_length=20, null=True, blank=True)
	domain_name = models.CharField(max_length=30, null=True, blank=True)
	pc_name = models.CharField(max_length=20, null=True, blank=True)
	office_pass = models.CharField(max_length=10, null=True, blank=True)
	address_ip_phone = models.CharField(max_length=20, null=True, blank=True)
	address_ip_phone_second = models.CharField(max_length=20, null=True, blank=True)
	phone_pass = models.CharField(max_length=20, null=True, blank=True)
	
	def __str__(self):
		return self.name + ' ' + self.surname
