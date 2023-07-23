from django.contrib.auth import get_user_model
from django.db import models
from dental_clinic.patient.models import Patient


UserModel = get_user_model()


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    dentist = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
