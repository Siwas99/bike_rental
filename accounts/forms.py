from django import forms
from django.contrib.auth.forms import UserCreationForm, AdminUserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from django.db import transaction

from accounts.models import CustomUser, Address
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
    email = forms.EmailField(required=True, label="Email address")

    address_line1 = forms.CharField(max_length=100)
    address_line2 = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100, initial="Poland")
    region = forms.CharField(max_length=100)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("email","phone_number", "birth_date")
        labels = {
            'username': 'Username',
            'phone_number': 'Phone number',
            'birth_date': 'Date of birth',
        }
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date'}
            ),
        }

    @transaction.atomic
    def save(self, commit = True):
        user = super().save(commit=False)
        user.phone_number = self.cleaned_data['phone_number']
        user.birth_date = self.cleaned_data['birth_date']

        if commit:
            user.save()
            self.save_m2m()

            if "groups" not in self.fields:
                customer_group = Group.objects.get(name="customer")
                user.groups.add(customer_group)

            Address.objects.create(
                user=user,
                address_line1=self.cleaned_data["address_line1"],
                address_line2=self.cleaned_data["address_line2"],
                postal_code=self.cleaned_data["postal_code"],
                city=self.cleaned_data["city"],
                country=self.cleaned_data["country"],
            )

        return user

class ManagerUserCreateForm(CustomUserCreateForm):
    class Meta(CustomUserCreateForm.Meta):
        fields = CustomUserCreateForm.Meta.fields + ("groups",)

class CustomUserUpdateForm(CustomUserValidationMixin, forms.ModelForm):
    email = forms.EmailField(required=True, label="Email address")

    address_line1 = forms.CharField(max_length=100, required=False)
    address_line2 = forms.CharField(max_length=100, required=False)
    postal_code = forms.CharField(max_length=10, required=False)
    city = forms.CharField(max_length=100, required=False)
    country = forms.CharField(max_length=100, required=False)
    region = forms.CharField(max_length=100, required=False)

    ADDRESS_FIELDS = (
        "address_line1",
        "address_line2",
        "postal_code",
        "city",
        "country",
        "region",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if(self.instance.pk):
            address = Address.objects.filter(user=self.instance).first()
            print(address)
            if address:
                for field in self.ADDRESS_FIELDS:
                    self.initial.setdefault(field, getattr(address, field))

    @transaction.atomic
    def save(self, commit = True):
        user = super().save(commit = False)

        if commit:
            user.save()
            self.save_m2m()

            Address.objects.update_or_create(
                user=user,
                defaults={
                    field: self.cleaned_data[field]
                    for field in self.ADDRESS_FIELDS
                },
            )

        return user

    class Meta:
        model = CustomUser
        fields = ("email", "phone_number", "birth_date")
        labels = {
            'username': 'Username',
            'phone_number': 'Phone number',
            'birth_date': 'Date of birth',
        }
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date'}
            ),
        }

class CustomUserAdminChangeForm(CustomUserValidationMixin,UserChangeForm,):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = "__all__"

class ManagerUserUpdateForm(CustomUserUpdateForm):
    class Meta(CustomUserUpdateForm.Meta):
        fields = CustomUserUpdateForm.Meta.fields + ("groups",)

class CustomUserAdminForm(CustomUserValidationMixin, AdminUserCreationForm):
    class Meta:
        model = CustomUser
        fields = AdminUserCreationForm.Meta.fields + ("phone_number", "birth_date")
