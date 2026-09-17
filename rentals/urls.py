from django.urls import path

from rentals.views import BikeDetailView, BikeListView, RentalListView, RentalDetailView, RentalCreateView, \
    RentalUpdateView, BikeCreateView, BikeUpdateView

urlpatterns = [
    path('', RentalListView.as_view(), name='rentals'),
    path('<int:pk>/', RentalDetailView.as_view(), name='rental-detail'),
    path('create/', RentalCreateView.as_view(), name='rental-create'),
    path('<int:pk>/update/', RentalUpdateView.as_view(), name='rental-update'),
    path('bikes/', BikeListView.as_view(), name='bikes'),
    path('bikes/<int:pk>/', BikeDetailView.as_view(), name='bike-detail'),
    path('bikes/create/', BikeCreateView.as_view(), name='bike-create'),
    path('bikes/<int:pk>/update/', BikeUpdateView.as_view(), name='bike-update'),
]
