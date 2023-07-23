from django.db import models
from dental_clinic.patient.models import Patient


class Invoice(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    invoice_number = models.CharField(primary_key=True, max_length=10)
    date_issued = models.DateField(auto_now_add=True)
    amount = models.CharField(max_length=10)


    def __str__(self):
        return f"{self.invoice_number}"
