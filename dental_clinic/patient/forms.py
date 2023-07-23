from django import forms
from .models import Patient


class AddTreatmentForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['treatment']
