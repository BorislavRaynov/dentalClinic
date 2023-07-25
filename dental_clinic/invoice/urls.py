from django.urls import path
from .views import generate_invoice


urlpatterns = [
    path('<int:appointment_pk>/<int:patient_pk>', generate_invoice, name='invoicing')
]
