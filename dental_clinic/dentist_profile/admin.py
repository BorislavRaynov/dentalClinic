from django.contrib import admin
from dental_clinic.dentist_profile.models import DentistUserProfile


@admin.register(DentistUserProfile)
class AppointmentAdmin(admin.ModelAdmin):
    ordering = ('first_name',)