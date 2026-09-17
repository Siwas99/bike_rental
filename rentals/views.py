from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse

from rentals.forms import BikeForm, RentalForm
from rentals.models import Rental, Bike


class DetailRedirectMixin:
    detail_url_name = None

    def get_success_url(self):
        return reverse(self.detail_url_name, args=[self.object.pk])

# RENTALS
class RentalListView(ListView):
    model = Rental
    template_name = 'rental_list.html'
    context_object_name = 'rentals'
    queryset = Rental.objects.select_related('bike', 'user').order_by('-rental_date', '-pk')

class RentalDetailView(DetailView):
    model = Rental
    template_name = 'rental_detail.html'
    context_object_name = 'rental'
    queryset = Rental.objects.select_related('bike', 'user')

class RentalCreateView(DetailRedirectMixin, CreateView):
    model = Rental
    form_class = RentalForm
    detail_url_name = 'rental-detail'
    template_name = 'rental_form.html'

class RentalUpdateView(DetailRedirectMixin, UpdateView):
    model = Rental
    form_class = RentalForm
    detail_url_name = 'rental-detail'
    template_name = 'rental_form.html'


# BIKES
class BikeListView(ListView):
    model = Bike
    template_name = 'bike_list.html'
    context_object_name = 'bikes'
    ordering = ['name', 'pk']

class BikeDetailView(DetailView):
    model = Bike
    template_name = 'bike_detail.html'
    context_object_name = 'bike'

class BikeCreateView(DetailRedirectMixin, CreateView):
    model = Bike
    form_class = BikeForm
    detail_url_name = 'bike-detail'
    template_name = 'bike_form.html'

class BikeUpdateView(DetailRedirectMixin, UpdateView):
    model = Bike
    form_class = BikeForm
    detail_url_name = 'bike-detail'
    template_name = 'bike_form.html'
