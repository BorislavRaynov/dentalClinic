from django.urls import path
from .views import PatientCreateView, PatientEditView, PatientAddTreatment, PatientListView, \
    PatientMedicalRecordView, \
    MedicalConditionCreateView, MedicalConditionUpdateView, MedicalConditionDeleteView, \
    AllergyCreateView, AllergyUpdateView, AllergyDeleteView, \
    MedicalHistoryEntryCreateView, MedicalHistoryEntryUpdateView, MedicalHistoryEntryDeleteView


urlpatterns = [
    path('', PatientListView.as_view(), name='patients-catalogue'),
    path('create/', PatientCreateView.as_view(), name='create-patient'),
    path('edit/<int:pk>', PatientEditView.as_view(), name='edit-patient'),
    path('addtreatments/<int:pk>', PatientAddTreatment.as_view(), name='patient-treatment'),
    path('<int:pk>/medical/', PatientMedicalRecordView.as_view(), name='patient-medical-record'),

    path('<int:patient_pk>/conditions/add/', MedicalConditionCreateView.as_view(), name='condition-add'),
    path('conditions/<int:pk>/edit/', MedicalConditionUpdateView.as_view(), name='condition-edit'),
    path('conditions/<int:pk>/delete/', MedicalConditionDeleteView.as_view(), name='condition-delete'),

    path('<int:patient_pk>/allergies/add/', AllergyCreateView.as_view(), name='allergy-add'),
    path('allergies/<int:pk>/edit/', AllergyUpdateView.as_view(), name='allergy-edit'),
    path('allergies/<int:pk>/delete/', AllergyDeleteView.as_view(), name='allergy-delete'),

    path('<int:patient_pk>/history/add/', MedicalHistoryEntryCreateView.as_view(), name='history-add'),
    path('history/<int:pk>/edit/', MedicalHistoryEntryUpdateView.as_view(), name='history-edit'),
    path('history/<int:pk>/delete/', MedicalHistoryEntryDeleteView.as_view(), name='history-delete'),
]
