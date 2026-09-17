from django.contrib.auth.models import User
from django.db import models

from django_project import settings

# Create your models here.
class Bike(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    production_year = models.IntegerField()
    purchase_date = models.DateField()
    serial_number = models.CharField(max_length=50)
    price_per_day = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.manufacturer}"

class Rental(models.Model):
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    rental_date = models.DateField()
    planned_return_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.bike.name} rented by {self.user.username}"