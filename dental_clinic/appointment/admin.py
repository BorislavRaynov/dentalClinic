from django.contrib import admin
from dental_clinic.appointment.models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'dentist', 'date', 'time']
    ordering = ['date', 'time']
    search_fields = ['dentist']
    list_filter = ['date']
