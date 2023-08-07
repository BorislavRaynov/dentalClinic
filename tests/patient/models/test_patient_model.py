from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from dental_clinic.patient.models import Patient
from dental_clinic.treatment.models import Treatment


class PatientModelTestCase(TestCase):

    VALID_PATIENT_DATA = {
        "email": "test@test.com",
        "first_name": "Firstname",
        "last_name": "Lastname",
        "phone_number": "1234567890",
    }

    def test_create_patient_with_valid_data(self):
        patient = Patient.objects.create(**self.VALID_PATIENT_DATA)

        self.assertEqual(patient.email, "test@test.com")
        self.assertEqual(patient.first_name, "Firstname")
        self.assertEqual(patient.last_name, "Lastname")
        self.assertEqual(patient.phone_number, "1234567890")
        self.assertEqual(patient.treatment.count(), 0)

    def test_create_patient_with_invalid_phone_number_raises(self):
        with self.assertRaises(ValidationError):
            patient = Patient.objects.create(
                email="test@test.com",
                first_name="Firstname",
                last_name="Lastname",
                phone_number="123a456789"
            )
            patient.full_clean()

    def test_create_patient_with_non_capital_names_raises(self):
        with self.assertRaises(ValidationError):
            patient = Patient.objects.create(
                email="test@test.com",
                first_name="firstname",
                last_name="lastname",
                phone_number="1234567890"
            )
            patient.full_clean()

    def test_create_patient_with_non_letters_in_names_raises(self):
        with self.assertRaises(ValidationError):
            patient = Patient.objects.create(
                email="test@test.com",
                first_name="Firstname1",
                last_name="Lastname2",
                phone_number="1234567890"
            )
            patient.full_clean()

    def test_create_patient_with_existing_email_raises(self):
        patient1 = Patient.objects.create(**self.VALID_PATIENT_DATA)
        with self.assertRaises(IntegrityError):
            patient2 = Patient.objects.create(
                email="test@test.com",
                first_name="Otherfname",
                last_name="Otherlname",
                phone_number="9876543210"
            )
            patient2.full_clean()
