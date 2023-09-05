from django.contrib import admin
from dental_clinic.treatment.models import Treatment


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ['clinical_code', 'cost', 'name', 'description']
    ordering = ['clinical_code']
    search_fields = ['description']
