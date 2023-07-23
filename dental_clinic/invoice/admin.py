from django.contrib import admin
from dental_clinic.invoice.models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'amount', 'patient', 'date_issued']
    list_filter = ['date_issued']
    search_fields = ['patient']
    ordering = ['-invoice_number']
