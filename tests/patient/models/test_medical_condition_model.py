from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from dental_clinic.patient.models import MedicalCondition, Patient


class MedicalConditionModelTestCase(TestCase):

    def setUp(self):
        self.patient = Patient.objects.create(
            email="patient@test.com",
            first_name="Firstname",
            last_name="Lastname",
            phone_number="1234567890",
        )

    def test_create_medical_condition_with_valid_data(self):
        condition = MedicalCondition.objects.create(
            patient=self.patient,
            name="Diabetes",
            status=MedicalCondition.STATUS_ACTIVE,
            diagnosed_date=timezone.localdate(),
            notes="Type 2",
        )

        self.assertEqual(condition.name, "Diabetes")
        self.assertEqual(condition.status, MedicalCondition.STATUS_ACTIVE)
        self.assertEqual(condition.notes, "Type 2")
        self.assertEqual(condition.patient, self.patient)

    def test_medical_condition_status_defaults_to_active(self):
        condition = MedicalCondition.objects.create(patient=self.patient, name="Diabetes")

        self.assertEqual(condition.status, MedicalCondition.STATUS_ACTIVE)

    def test_medical_condition_with_future_diagnosed_date_raises_on_full_clean(self):
        future_date = timezone.localdate() + timedelta(days=1)
        condition = MedicalCondition.objects.create(
            patient=self.patient, name="Diabetes", diagnosed_date=future_date
        )

        with self.assertRaises(ValidationError):
            condition.full_clean()

    def test_medical_condition_str_representation(self):
        condition = MedicalCondition.objects.create(
            patient=self.patient, name="Diabetes", status=MedicalCondition.STATUS_RESOLVED
        )

        self.assertEqual(str(condition), "Diabetes (resolved)")

    def test_medical_condition_reverse_access_via_patient(self):
        condition = MedicalCondition.objects.create(patient=self.patient, name="Diabetes")

        self.assertIn(condition, self.patient.medical_conditions.all())

    def test_deleting_patient_cascades_to_medical_conditions(self):
        MedicalCondition.objects.create(patient=self.patient, name="Diabetes")

        self.patient.delete()

        self.assertEqual(MedicalCondition.objects.count(), 0)
