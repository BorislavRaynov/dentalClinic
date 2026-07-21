from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from dental_clinic.patient.models import MedicalHistoryEntry, Patient


class MedicalHistoryEntryModelTestCase(TestCase):

    def setUp(self):
        self.patient = Patient.objects.create(
            email="patient@test.com",
            first_name="Firstname",
            last_name="Lastname",
            phone_number="1234567890",
        )

    def test_create_medical_history_entry_with_valid_data(self):
        entry = MedicalHistoryEntry.objects.create(
            patient=self.patient, entry_date=timezone.localdate(), note="Routine checkup"
        )

        self.assertEqual(entry.note, "Routine checkup")
        self.assertEqual(entry.entry_date, timezone.localdate())
        self.assertEqual(entry.patient, self.patient)

    def test_medical_history_entry_with_future_entry_date_raises_on_full_clean(self):
        future_date = timezone.localdate() + timedelta(days=1)
        entry = MedicalHistoryEntry.objects.create(
            patient=self.patient, entry_date=future_date, note="Future note"
        )

        with self.assertRaises(ValidationError):
            entry.full_clean()

    def test_medical_history_entry_date_defaults_to_today(self):
        entry = MedicalHistoryEntry.objects.create(patient=self.patient, note="Routine checkup")

        self.assertEqual(entry.entry_date, timezone.localdate())

    def test_medical_history_entries_ordered_by_entry_date_descending(self):
        older = MedicalHistoryEntry.objects.create(
            patient=self.patient,
            entry_date=timezone.localdate() - timedelta(days=5),
            note="Older",
        )
        newer = MedicalHistoryEntry.objects.create(
            patient=self.patient,
            entry_date=timezone.localdate() - timedelta(days=1),
            note="Newer",
        )

        entries = list(MedicalHistoryEntry.objects.all())

        self.assertEqual(entries, [newer, older])

    def test_medical_history_entry_str_representation(self):
        entry = MedicalHistoryEntry.objects.create(
            patient=self.patient, entry_date=timezone.localdate(), note="Routine checkup"
        )

        self.assertEqual(str(entry), f"{self.patient} - {entry.entry_date}")

    def test_medical_history_entry_reverse_access_via_patient(self):
        entry = MedicalHistoryEntry.objects.create(patient=self.patient, note="Routine checkup")

        self.assertIn(entry, self.patient.medical_history_entries.all())

    def test_deleting_patient_cascades_to_medical_history_entries(self):
        MedicalHistoryEntry.objects.create(patient=self.patient, note="Routine checkup")

        self.patient.delete()

        self.assertEqual(MedicalHistoryEntry.objects.count(), 0)
