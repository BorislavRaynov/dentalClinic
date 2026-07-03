from django.urls import path
from .views import TreatmentCreateView, TreatmentEditView


urlpatterns = [
    path('create/', TreatmentCreateView.as_view(), name='treatment-create'),
    path('edit/<int:pk>', TreatmentEditView.as_view(), name='treatment-edit'),
]
