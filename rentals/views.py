from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse

from rentals.forms import BikeForm, RentalCrateForm, RentalUpdateForm
from rentals.models import Rental, Bike


class DetailRedirectMixin:
    detail_url_name = None

    def get_success_url(self):
        return reverse(self.detail_url_name, args=[self.object.pk])

# RENTALS
class RentalListView(LoginRequiredMixin, ListView):
    model = Rental
    template_name = 'rental_list.html'
    context_object_name = 'rentals'
    queryset = Rental.objects.select_related('bike', 'user').order_by('-rental_date', '-pk')

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        if status:
            if status == 'ongoing':
                queryset = queryset.filter(return_date__isnull=True)
            elif status == 'returned':
                queryset = queryset.filter(return_date__isnull=False)

        if self.request.user.is_superuser | self.request.user.is_staff:
            return queryset

        return queryset.filter(user=self.request.user)

class RentalDetailView(LoginRequiredMixin, DetailView):
    model = Rental
    template_name = 'rental_detail.html'
    context_object_name = 'rental'
    queryset = Rental.objects.select_related('bike', 'user')

class RentalCreateView(LoginRequiredMixin, DetailRedirectMixin, CreateView):
    model = Rental
    form_class = RentalCrateForm
    detail_url_name = 'rental-detail'
    template_name = 'rental_form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        unavailable_bikes = Bike.objects.filter(
            rental__rental_date__isnull=False,
            rental__return_date__isnull=True
        )

        form.fields['bike'].queryset = form.fields['bike'].queryset.exclude(pk__in=unavailable_bikes)

        return form

class RentalUpdateView(LoginRequiredMixin, DetailRedirectMixin, UpdateView):
    model = Rental
    form_class = RentalUpdateForm
    detail_url_name = 'rental-detail'
    template_name = 'rental_form.html'

# BIKES
class BikeListView(ListView):
    model = Bike
    template_name = 'bike_list.html'
    context_object_name = 'bikes'
    ordering = ['name', 'pk']

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        if status:
            rentals = Rental.objects.select_related('bike')
            if status == 'available':
                queryset = queryset.exclude(pk__in=rentals.values_list('bike', flat=True))
            elif status == 'rented':
                queryset = queryset.filter(pk__in=rentals.values_list('bike', flat=True))

        return queryset

class BikeDetailView(DetailView):
    model = Bike
    template_name = 'bike_detail.html'
    context_object_name = 'bike'

class BikeCreateView(LoginRequiredMixin, DetailRedirectMixin, CreateView):
    model = Bike
    form_class = BikeForm
    detail_url_name = 'bike-detail'
    template_name = 'bike_form.html'

class BikeUpdateView(LoginRequiredMixin, DetailRedirectMixin, UpdateView):
    model = Bike
    form_class = BikeForm
    detail_url_name = 'bike-detail'
    template_name = 'bike_form.html'
