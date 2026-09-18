from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from accounts.forms import CustomUserCreateForm, CustomUserUpdateForm
from accounts.models import CustomUser
from rentals.models import Rental


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
    success_url = reverse_lazy('login')

class CustomUserUpdateProfile(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    template_name = 'custom_user_form.html'
    form_class = CustomUserUpdateForm
    success_url = reverse_lazy('user_profile')

    def get_object(self, queryset=None):
        return self.request.user

    def test_func(self):
        return self.request.user == self.get_object()

class UserProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'user_profile.html'
    context_object_name = 'custom_user'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rentals'] = Rental.objects.filter(user=self.request.user)
        context['username'] = self.object.username
        return context
