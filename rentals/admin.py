from django.contrib import admin

from rentals.models import Rental, Bike

# Register your models here.
admin.site.register(Rental)
admin.site.register(Bike)
