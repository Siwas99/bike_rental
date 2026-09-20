from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    birth_date = models.DateField(null=True, blank=True)

class Address(models.Model):
    address_line1 = models.CharField(max_length=100, null=True, blank=True)
    address_line2 = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="address"
    )
    def __str__(self):
        return self.address_line1 or "Brak adresu"