from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from django.test import TestCase
from django.utils import timezone

from dental_clinic.appointment.models import Appointment
from dental_clinic.auth_app.models import DentistUser
from dental_clinic.patient.models import Patient, TreatmentRecord
from dental_clinic.treatment.models import Treatment


class TreatmentRecordModelTestCase(TestCase):

    def setUp(self):
        self.patient = Patient.objects.create(
            email="patient@test.com",
            first_name="Firstname",
            last_name="Lastname",
            phone_number="1234567890",
        )
        self.treatment = Treatment.objects.create(
            clinical_code="123",
            name="Filling",
            cost=100.0,
            description="Composite filling",
        )
        self.dentist = DentistUser.objects.create_user(
            uin_number='9876543102', password='testpassword'
        )
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            dentist=self.dentist,
            date=timezone.localdate(),
            time="10:00:00",
        )

    def test_create_treatment_record_with_valid_data(self):
        record = TreatmentRecord.objects.create(
            patient=self.patient,
            treatment=self.treatment,
            appointment=self.appointment,
            performed_by=self.dentist,
            date_performed=timezone.localdate(),
            tooth="14",
            notes="Straightforward filling",
        )
        record.full_clean()

        self.assertEqual(record.patient, self.patient)
        self.assertEqual(record.treatment, self.treatment)
        self.assertEqual(record.appointment, self.appointment)
        self.assertEqual(record.performed_by, self.dentist)
        self.assertEqual(record.tooth, "14")
        self.assertEqual(record.notes, "Straightforward filling")

    def test_treatment_record_date_performed_is_nullable(self):
        record = TreatmentRecord.objects.create(patient=self.patient, treatment=self.treatment)
        record.full_clean()

        self.assertIsNone(record.date_performed)

    def test_treatment_record_with_future_date_performed_raises_on_full_clean(self):
        future_date = timezone.localdate() + timedelta(days=1)
        record = TreatmentRecord.objects.create(
            patient=self.patient, treatment=self.treatment, date_performed=future_date
        )

        with self.assertRaises(ValidationError):
            record.full_clean()

    def test_deleting_referenced_treatment_is_protected(self):
        TreatmentRecord.objects.create(patient=self.patient, treatment=self.treatment)

        with self.assertRaises(ProtectedError):
            self.treatment.delete()

    def test_deleting_appointment_sets_null_on_treatment_record(self):
        record = TreatmentRecord.objects.create(
            patient=self.patient, treatment=self.treatment, appointment=self.appointment
        )

        self.appointment.delete()
        record.refresh_from_db()

        self.assertIsNone(record.appointment)

    def test_deleting_performed_by_sets_null_on_treatment_record(self):
        record = TreatmentRecord.objects.create(
            patient=self.patient, treatment=self.treatment, performed_by=self.dentist
        )

        self.dentist.delete()
        record.refresh_from_db()

        self.assertIsNone(record.performed_by)

    def test_treatment_records_ordered_by_date_performed_descending(self):
        older = TreatmentRecord.objects.create(
            patient=self.patient,
            treatment=self.treatment,
            date_performed=timezone.localdate() - timedelta(days=5),
        )
        newer = TreatmentRecord.objects.create(
            patient=self.patient,
            treatment=self.treatment,
            date_performed=timezone.localdate() - timedelta(days=1),
        )

        records = list(TreatmentRecord.objects.all())

        self.assertEqual(records, [newer, older])

    def test_treatment_record_str_representation(self):
        record = TreatmentRecord.objects.create(
            patient=self.patient, treatment=self.treatment, date_performed=timezone.localdate()
        )

        self.assertEqual(
            str(record), f"{self.treatment} on {self.patient} ({record.date_performed})"
        )

    def test_treatment_record_str_representation_without_date_performed(self):
        record = TreatmentRecord.objects.create(patient=self.patient, treatment=self.treatment)

        self.assertEqual(str(record), f"{self.treatment} on {self.patient} (unknown)")

    def test_treatment_record_reverse_access_via_patient(self):
        record = TreatmentRecord.objects.create(patient=self.patient, treatment=self.treatment)

        self.assertIn(record, self.patient.treatment_records.all())

    def test_deleting_patient_cascades_to_treatment_records(self):
        TreatmentRecord.objects.create(patient=self.patient, treatment=self.treatment)

        self.patient.delete()

        self.assertEqual(TreatmentRecord.objects.count(), 0)
