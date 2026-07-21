from datetime import timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.utils import timezone
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

    def test_patient_id_is_auto_generated_with_expected_prefix_and_length(self):
        patient = Patient.objects.create(**self.VALID_PATIENT_DATA)

        self.assertTrue(patient.patient_id.startswith(Patient.PATIENT_ID_PREFIX))
        self.assertEqual(len(patient.patient_id), Patient.PATIENT_ID_MAX_LENGTH)

    def test_two_patients_get_distinct_patient_ids(self):
        patient1 = Patient.objects.create(**self.VALID_PATIENT_DATA)
        patient2 = Patient.objects.create(
            email="second@test.com",
            first_name="Secondname",
            last_name="Otherlastname",
            phone_number="1112223333",
        )

        self.assertNotEqual(patient1.patient_id, patient2.patient_id)

    def test_create_patient_with_future_date_of_birth_raises_on_full_clean(self):
        future_date = timezone.localdate() + timedelta(days=1)
        patient = Patient.objects.create(
            email="future@test.com",
            first_name="Futurename",
            last_name="Personlast",
            phone_number="1234567890",
            date_of_birth=future_date,
        )

        with self.assertRaises(ValidationError):
            patient.full_clean()

    def test_create_patient_with_todays_date_of_birth_is_valid(self):
        today = timezone.localdate()
        patient = Patient.objects.create(
            email="today@test.com",
            first_name="Todayname",
            last_name="Personlast",
            phone_number="1234567890",
            date_of_birth=today,
        )

        patient.full_clean()

        self.assertEqual(patient.date_of_birth, today)

    def test_create_patient_without_optional_fields_is_valid(self):
        patient = Patient.objects.create(**self.VALID_PATIENT_DATA)

        patient.full_clean()

        self.assertEqual(patient.address, "")
        self.assertIsNone(patient.date_of_birth)
        self.assertEqual(patient.sex, "")
