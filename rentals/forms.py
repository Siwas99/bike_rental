from django import forms

from rentals.models import Bike, Rental


class BikeForm(forms.ModelForm):
    class Meta:
        model = Bike
        fields = ['name', 'manufacturer', 'production_year', 'purchase_date',
                  'serial_number', 'price_per_day', 'is_active']
        labels = {
            'name': 'Name / model', 'manufacturer': 'Manufacturer',
            'production_year': 'Year of manufacture', 'purchase_date': 'Purchase date',
            'serial_number': 'Serial number', 'price_per_day': 'Price per day (PLN)',
            'is_active': 'Active bike',
        }
        help_texts = {'is_active': 'Select if the bike belongs to the active fleet.'}
        widgets = {
            'purchase_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }


class RentalCrateForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['bike', 'user', 'rental_date', 'planned_return_date', 'return_date']
        labels = {'bike': 'Bike', 'user': 'User',
                  'rental_date': 'Rental date',
                  'planned_return_date': 'Planned return date',
                  'return_date': 'Return date'
                  }
        help_texts = {'return_date': 'Leave blank if the bike is still out on a ride.'}
        widgets = {
            'rental_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'planned_return_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'return_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned = super().clean()
        start, end = cleaned.get('rental_date'), cleaned.get('return_date')
        if start and end and end < start:
            self.add_error('return_date', 'The return date cannot be earlier than the rental date.')
        return cleaned

class RentalUpdateForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['user', 'rental_date', 'planned_return_date', 'return_date']
        labels = {'user': 'User',
                  'rental_date': 'Rental date',
                  'planned_return_date': 'Planned return date',
                  'return_date': 'Return date'
                  }
        help_texts = {'return_date': 'Leave blank if the bike is still out on a ride.'}
        widgets = {
            'rental_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'planned_return_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'return_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned = super().clean()
        start, end = cleaned.get('rental_date'), cleaned.get('return_date')
        if start and end and end < start:
            self.add_error('return_date', 'The return date cannot be earlier than the rental date.')
        return cleaned
