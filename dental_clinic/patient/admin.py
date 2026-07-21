from django.contrib import admin
from dental_clinic.patient.models import Patient, MedicalCondition, Allergy, MedicalHistoryEntry, \
    ClinicalNote, Prescription, TreatmentRecord


class MedicalConditionInline(admin.TabularInline):
    model = MedicalCondition
    extra = 0


class AllergyInline(admin.TabularInline):
    model = Allergy
    extra = 0


class MedicalHistoryEntryInline(admin.TabularInline):
    model = MedicalHistoryEntry
    extra = 0


class ClinicalNoteInline(admin.TabularInline):
    model = ClinicalNote
    extra = 0


class PrescriptionInline(admin.TabularInline):
    model = Prescription
    extra = 0


class TreatmentRecordInline(admin.TabularInline):
    model = TreatmentRecord
    extra = 0


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'email', 'patient_id', 'date_of_birth')
    search_fields = ('patient_id', 'first_name', 'last_name', 'email', 'phone_number')
    inlines = (
        MedicalConditionInline, AllergyInline, MedicalHistoryEntryInline,
        ClinicalNoteInline, PrescriptionInline, TreatmentRecordInline,
    )
