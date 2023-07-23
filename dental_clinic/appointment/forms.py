from django import forms
from .models import Appointment


class AppointmentCreateForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'date', 'time', 'dentist']

        widgets = {

            'date': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'time': forms.TimeInput(
                attrs={'type': 'time'}),

            'dentist': forms.HiddenInput()
        }


class AppointmentEditForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time']

        widgets = {

            'date': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'time': forms.TimeInput(
                attrs={'type': 'time'})
        }
