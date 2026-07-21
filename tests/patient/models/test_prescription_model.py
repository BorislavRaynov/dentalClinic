from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from dental_clinic.auth_app.models import DentistUser
from dental_clinic.patient.models import Patient, Prescription


class PrescriptionModelTestCase(TestCase):

    def setUp(self):
        self.patient = Patient.objects.create(
            email="patient@test.com",
            first_name="Firstname",
            last_name="Lastname",
            phone_number="1234567890",
        )
        self.prescriber = DentistUser.objects.create_user(
            uin_number='9876543102', password='testpassword'
        )

    def test_create_prescription_with_valid_data(self):
        prescription = Prescription.objects.create(
            patient=self.patient,
            prescribed_by=self.prescriber,
            medication="Amoxicillin",
            dosage="500mg",
            instructions="Take three times daily",
        )
        prescription.full_clean()

        self.assertEqual(prescription.medication, "Amoxicillin")
        self.assertEqual(prescription.dosage, "500mg")
        self.assertEqual(prescription.instructions, "Take three times daily")
        self.assertEqual(prescription.patient, self.patient)
        self.assertEqual(prescription.prescribed_by, self.prescriber)

    def test_prescription_date_prescribed_defaults_to_today(self):
        prescription = Prescription.objects.create(
            patient=self.patient, medication="Amoxicillin", dosage="500mg"
        )

        self.assertEqual(prescription.date_prescribed, timezone.localdate())

    def test_prescription_with_future_date_prescribed_raises_on_full_clean(self):
        future_date = timezone.localdate() + timedelta(days=1)
        prescription = Prescription.objects.create(
            patient=self.patient,
            medication="Amoxicillin",
            dosage="500mg",
            date_prescribed=future_date,
        )

        with self.assertRaises(ValidationError):
            prescription.full_clean()

    def test_prescriptions_ordered_by_date_prescribed_descending(self):
        older = Prescription.objects.create(
            patient=self.patient,
            medication="Older",
            dosage="10mg",
            date_prescribed=timezone.localdate() - timedelta(days=5),
        )
        newer = Prescription.objects.create(
            patient=self.patient,
            medication="Newer",
            dosage="20mg",
            date_prescribed=timezone.localdate() - timedelta(days=1),
        )

        prescriptions = list(Prescription.objects.all())

        self.assertEqual(prescriptions, [newer, older])

    def test_prescription_str_representation(self):
        prescription = Prescription.objects.create(
            patient=self.patient, medication="Amoxicillin", dosage="500mg"
        )

        self.assertEqual(str(prescription), "Amoxicillin (500mg)")

    def test_prescription_reverse_access_via_patient(self):
        prescription = Prescription.objects.create(
            patient=self.patient, medication="Amoxicillin", dosage="500mg"
        )

        self.assertIn(prescription, self.patient.prescriptions.all())

    def test_deleting_patient_cascades_to_prescriptions(self):
        Prescription.objects.create(
            patient=self.patient, medication="Amoxicillin", dosage="500mg"
        )

        self.patient.delete()

        self.assertEqual(Prescription.objects.count(), 0)

    def test_deleting_prescriber_sets_null_on_prescription(self):
        prescription = Prescription.objects.create(
            patient=self.patient,
            prescribed_by=self.prescriber,
            medication="Amoxicillin",
            dosage="500mg",
        )

        self.prescriber.delete()
        prescription.refresh_from_db()

        self.assertIsNone(prescription.prescribed_by)
