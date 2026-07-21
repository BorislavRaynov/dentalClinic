from django import forms
from .models import Patient, MedicalCondition, Allergy, MedicalHistoryEntry


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'address', 'sex']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class AddTreatmentForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['treatment']


class MedicalConditionForm(forms.ModelForm):
    class Meta:
        model = MedicalCondition
        exclude = ['patient']


class AllergyForm(forms.ModelForm):
    class Meta:
        model = Allergy
        exclude = ['patient']


class MedicalHistoryEntryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistoryEntry
        exclude = ['patient']
