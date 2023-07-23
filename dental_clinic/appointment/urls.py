from django.urls import path
from .views import AppointmentDetailsView, \
    AppointmentCreateView, \
    AppointmentUpdateView, \
    AppointmentListView, \
    AppointmentDeleteView


urlpatterns = [
    path('details/<int:pk>/', AppointmentDetailsView.as_view(), name='appointment-details'),
    path('create/', AppointmentCreateView.as_view(), name='appointment-create'),
    path('edit/<int:pk>/', AppointmentUpdateView.as_view(), name='appointment-edit'),
    path('delete/<int:pk>/', AppointmentDeleteView.as_view(), name='appointment-delete'),
    path('list-all/', AppointmentListView.as_view(), name='appointments-catalogue')
]