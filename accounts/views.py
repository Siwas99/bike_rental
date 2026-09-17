from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from accounts.forms import CustomUserCreateForm, CustomUserUpdateForm
from accounts.models import CustomUser

# Create your views here.
class CustomUserListView(ListView):
    model = CustomUser
    template_name = 'custom_user_list.html'
    context_object_name = 'custom_users'

class CustomUserDetailView(DetailView):
    model = CustomUser
    template_name = 'custom_user_detail.html'
    context_object_name = 'custom_user'

class CustomUserCreateView(CreateView):
    model = CustomUser
    template_name = 'custom_user_form.html'
    form_class = CustomUserCreateForm
    success_url = reverse_lazy('custom_user_list')

class CustomUserUpdateView(UpdateView):
    model = CustomUser
    template_name = 'custom_user_form.html'
    form_class = CustomUserUpdateForm
    success_url = reverse_lazy('custom_user_list')

class CustomUserDeleteView(DeleteView):
    model = CustomUser
    template_name = 'custom_user_confirm_delete.html'
    success_url = reverse_lazy('custom_user_list')

class CustomUserSignUpView(CreateView):
    model = CustomUser
    template_name = 'registration/signup.html'
    form_class = CustomUserCreateForm
    success_url = revere_lazy('login')