from django import forms

from rentals.models import Bike, Rental


class BikeForm(forms.ModelForm):
    class Meta:
        model = Bike
        fields = ['name', 'manufacturer', 'production_year', 'purchase_date',
                  'serial_number', 'price_per_day', 'is_active']
        labels = {
            'name': 'Nazwa / model', 'manufacturer': 'Producent',
            'production_year': 'Rok produkcji', 'purchase_date': 'Data zakupu',
            'serial_number': 'Numer seryjny', 'price_per_day': 'Cena za dobę (zł)',
            'is_active': 'Rower aktywny',
        }
        help_texts = {'is_active': 'Zaznacz, jeśli rower należy do aktywnej floty.'}
        widgets = {
            'purchase_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }


class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['bike', 'user', 'rental_date', 'planned_return_date', 'return_date']
        labels = {'bike': 'Rower', 'user': 'Użytkownik',
                  'rental_date': 'Data wypożyczenia',
                  'planned_return_date': 'Planowane data wypożyczenia',
                  'return_date': 'Data zwrotu'
                  }
        help_texts = {'return_date': 'Pozostaw puste, jeśli rower jest jeszcze w trasie.'}
        widgets = {
            'rental_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'planned_return_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'return_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned = super().clean()
        start, end = cleaned.get('rental_date'), cleaned.get('return_date')
        if start and end and end < start:
            self.add_error('return_date', 'Data zwrotu nie może być wcześniejsza niż data wypożyczenia.')
        return cleaned
