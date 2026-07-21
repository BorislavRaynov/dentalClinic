import uuid

from django.conf import settings
from django.db import models, transaction
from django.db.utils import IntegrityError
from django.core.validators import MinLengthValidator
from django.utils import timezone
from .validators import validate_phone_number_only_nums, \
    validate_name_contain_only_letters, \
    validate_name_start_with_capital_letter, \
    validate_date_not_in_future
from ..treatment.models import Treatment


def generate_patient_id():
    return f"{Patient.PATIENT_ID_PREFIX}{uuid.uuid4().hex[:8].upper()}"


class Patient(models.Model):
    PATIENT_ID_MAX_LENGTH = 11
    PATIENT_ID_PREFIX = 'PT-'
    PATIENT_ID_MAX_ATTEMPTS = 5
    ADDRESS_MAX_LENGTH = 255

    SEX_MALE = 'M'
    SEX_FEMALE = 'F'
    SEX_OTHER = 'O'
    SEX_CHOICES = (
        (SEX_MALE, 'Male'),
        (SEX_FEMALE, 'Female'),
        (SEX_OTHER, 'Other'),
    )

    patient_id = models.CharField(
        max_length=PATIENT_ID_MAX_LENGTH,
        unique=True,
        editable=False,
        default=generate_patient_id,
    )

    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=30, validators=(
        validate_name_start_with_capital_letter, validate_name_contain_only_letters
    ))

    last_name = models.CharField(max_length=30, validators=(
        validate_name_start_with_capital_letter, validate_name_contain_only_letters
    ))

    phone_number = models.CharField(
        max_length=10,
        validators=[MinLengthValidator(10), validate_phone_number_only_nums]
    )

    address = models.CharField(max_length=ADDRESS_MAX_LENGTH, blank=True)

    date_of_birth = models.DateField(
        null=True, blank=True, validators=[validate_date_not_in_future]
    )

    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True)

    treatment = models.ManyToManyField(Treatment, blank=True)

    def save(self, *args, **kwargs):
        """Retry with a freshly generated patient_id on a collision.

        Only applies to brand-new rows: the auto-generated patient_id is
        assigned once at instantiation time, so a collision can only ever
        happen on INSERT, not on subsequent updates of an existing patient.
        """
        if not self._state.adding:
            return super().save(*args, **kwargs)

        for attempt in range(self.PATIENT_ID_MAX_ATTEMPTS):
            try:
                with transaction.atomic():
                    return super().save(*args, **kwargs)
            except IntegrityError:
                if attempt == self.PATIENT_ID_MAX_ATTEMPTS - 1:
                    raise
                self.patient_id = generate_patient_id()

    def delete(self, *args, **kwargs):
        self.treatment.clear()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class MedicalCondition(models.Model):
    NAME_MAX_LENGTH = 100
    CODE_MAX_LENGTH = 10

    STATUS_ACTIVE = 'active'
    STATUS_RESOLVED = 'resolved'
    STATUS_CHOICES = (
        (STATUS_ACTIVE, 'Active'),
        (STATUS_RESOLVED, 'Resolved'),
    )

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='medical_conditions'
    )
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    code = models.CharField(max_length=CODE_MAX_LENGTH, blank=True)
    status = models.CharField(
        max_length=8, choices=STATUS_CHOICES, default=STATUS_ACTIVE
    )
    diagnosed_date = models.DateField(
        null=True, blank=True, validators=[validate_date_not_in_future]
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f"{self.name} ({self.status})"


class Allergy(models.Model):
    NAME_MAX_LENGTH = 100

    SEVERITY_MILD = 'mild'
    SEVERITY_MODERATE = 'moderate'
    SEVERITY_SEVERE = 'severe'
    SEVERITY_CHOICES = (
        (SEVERITY_MILD, 'Mild'),
        (SEVERITY_MODERATE, 'Moderate'),
        (SEVERITY_SEVERE, 'Severe'),
    )

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='allergies'
    )
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    severity = models.CharField(
        max_length=8, choices=SEVERITY_CHOICES, default=SEVERITY_MILD
    )
    reaction = models.TextField(blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f"{self.name} - {self.severity}"


class MedicalHistoryEntry(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='medical_history_entries'
    )
    entry_date = models.DateField(
        default=timezone.localdate, validators=[validate_date_not_in_future]
    )
    note = models.TextField()

    class Meta:
        ordering = ('-entry_date',)

    def __str__(self):
        return f"{self.patient} - {self.entry_date}"


class ClinicalNote(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='clinical_notes'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='clinical_notes'
    )
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    body = models.TextField()

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.patient} note {self.created_at:%Y-%m-%d}"


class Prescription(models.Model):
    MEDICATION_MAX_LENGTH = 200
    DOSAGE_MAX_LENGTH = 100

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='prescriptions'
    )
    prescribed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='prescriptions'
    )
    medication = models.CharField(max_length=MEDICATION_MAX_LENGTH)
    dosage = models.CharField(max_length=DOSAGE_MAX_LENGTH)
    instructions = models.TextField(blank=True)
    date_prescribed = models.DateField(
        default=timezone.localdate, validators=[validate_date_not_in_future]
    )

    class Meta:
        ordering = ('-date_prescribed',)

    def __str__(self):
        return f"{self.medication} ({self.dosage})"


class TreatmentRecord(models.Model):
    TOOTH_MAX_LENGTH = 10

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='treatment_records'
    )
    treatment = models.ForeignKey(
        Treatment, on_delete=models.PROTECT, related_name='treatment_records'
    )
    appointment = models.ForeignKey(
        'appointment.Appointment', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='treatment_records'
    )
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='treatment_records'
    )
    date_performed = models.DateField(
        null=True, blank=True, validators=[validate_date_not_in_future]
    )
    tooth = models.CharField(max_length=TOOTH_MAX_LENGTH, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ('-date_performed',)

    def __str__(self):
        return f"{self.treatment} on {self.patient} ({self.date_performed or 'unknown'})"
