from django import forms
from django.contrib.auth.forms import UserCreationForm, AdminUserCreationForm

from accounts.models import CustomUser
from django.utils.timezone import localdate


class CustomUserValidationMixin:
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if CustomUser.objects.filter(phone_number=phone_number).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Phone number already exists.')
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Email number already exists.')
        return email

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        today = localdate()
        if birth_date and birth_date > today:
            raise forms.ValidationError('Birth date cannot be in the future.')
        return birth_date

class CustomUserCreateForm(CustomUserValidationMixin, UserCreationForm):
    email = forms.EmailField(required=True, label="Adres email")

    address_line1 = forms.CharField(max_length=100)
    address_line2 = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100, initial="Polska")
    region = forms.CharField(max_length=100)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("email","phone_number", "birth_date")
        labels = {
            'username': 'Nazwa użytkownika',
            'phone_number': 'Numer telefonu',
            'birth_date': 'Data urodzenia',
        }
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date'}
            ),
        }

class CustomUserUpdateForm(CustomUserValidationMixin, forms.ModelForm):
    email = forms.EmailField(required=True, label="Adres email")

    class Meta:
        model = CustomUser
        fields = ("email", "phone_number", "birth_date")
        labels = {
            'username': 'Nazwa użytkownika',
            'phone_number': 'Numer telefonu',
            'birth_date': 'Data urodzenia',
        }
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date'}
            ),
        }

class CustomUserAdminForm(CustomUserValidationMixin, AdminUserCreationForm):
    class Meta:
        model = CustomUser
        fields = AdminUserCreationForm.Meta.fields + ("phone_number", "birth_date")
