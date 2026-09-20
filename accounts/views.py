from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from accounts.forms import CustomUserCreateForm, CustomUserUpdateForm, ManagerUserCreateForm, ManagerUserUpdateForm
from accounts.models import CustomUser
from rentals.models import Rental


# Create your views here.
class CustomUserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'custom_user_list.html'
    context_object_name = 'custom_users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for user in context['custom_users']:
            user.rentalsCount = Rental.objects.filter(user=user).count()
            user.activeRentalsCount = Rental.objects.filter(
                user=user,
                return_date__isnull=True
            ).count()

        return context

class CustomUserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'custom_user_detail.html'
    context_object_name = 'custom_user'

class CustomUserCreateView(LoginRequiredMixin, CreateView):
    model = CustomUser
    template_name = 'custom_user_form.html'
    form_class = ManagerUserCreateForm
    success_url = reverse_lazy('custom_user_list')

class CustomUserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'custom_user_form.html'
    form_class = ManagerUserUpdateForm
    success_url = reverse_lazy('custom_user_list')

class CustomUserDeleteView(LoginRequiredMixin, DeleteView):
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
