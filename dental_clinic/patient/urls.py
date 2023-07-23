from django.urls import path
from .views import PatientCreateView, PatientEditView, PatientAddTreatment, PatientListView


urlpatterns = [
    path('', PatientListView.as_view(), name='patients-catalogue'),
    path('create/', PatientCreateView.as_view(), name='create-patient'),
    path('edit/<int:pk>', PatientEditView.as_view(), name='edit-patient'),
    path('addtreatments/<int:pk>', PatientAddTreatment.as_view(), name='patient-treatment')
]
