from django.test import TestCase
from .models import UsersIT


class UsersITTestCase(TestCase):
    def setUp(self):
        self.user = UsersIT.objects.create(
            name="John",
            surname="Doe",
            administration="IT",
            address_ip_pc="192.168.1.1",
            login="johndoe",
            domain_name="example.com",
            pc_name="PC-001",
            office_pass="password",
            address_ip_phone="192.168.1.100",
            address_ip_phone_second="192.168.1.101",
            phone_pass="phonepassword"
        )

    def test_user_creation(self):
        user = UsersIT.objects.get(name="John")
        self.assertEqual(user.surname, "Doe")
        self.assertEqual(user.administration, "IT")

    def test_user_update(self):
        user = UsersIT.objects.get(name="John")
        user.surname = "Smith"
        user.save()
        updated_user = UsersIT.objects.get(name="John")
        self.assertEqual(updated_user.surname, "Smith")

    def test_user_deletion(self):
        user = UsersIT.objects.get(name="John")
        user.delete()
        with self.assertRaises(UsersIT.DoesNotExist):
            UsersIT.objects.get(name="John")


