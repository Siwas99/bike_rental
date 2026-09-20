from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.forms import CustomUserAdminForm, CustomUserAdminChangeForm
from accounts.models import CustomUser, Address


# Register your models here.
class AddressInline(admin.StackedInline):
    model = Address
    extra = 1
    max_num = 1

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserAdminForm
    form = CustomUserAdminChangeForm
    model = CustomUser
    list_display = [
        "username",
        "email",
        "phone_number",
        "birth_date",
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("phone_number", "birth_date",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("email", "phone_number", "birth_date",)}),)
    inlines = [AddressInline]

admin.site.register(Address)