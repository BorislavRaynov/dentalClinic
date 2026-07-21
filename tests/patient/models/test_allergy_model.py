from django.test import TestCase

from dental_clinic.patient.models import Allergy, Patient


class AllergyModelTestCase(TestCase):

    def setUp(self):
        self.patient = Patient.objects.create(
            email="patient@test.com",
            first_name="Firstname",
            last_name="Lastname",
            phone_number="1234567890",
        )

    def test_create_allergy_with_valid_data(self):
        allergy = Allergy.objects.create(
            patient=self.patient,
            name="Penicillin",
            severity=Allergy.SEVERITY_SEVERE,
            reaction="Rash",
        )

        self.assertEqual(allergy.name, "Penicillin")
        self.assertEqual(allergy.severity, Allergy.SEVERITY_SEVERE)
        self.assertEqual(allergy.reaction, "Rash")
        self.assertEqual(allergy.patient, self.patient)

    def test_allergy_severity_defaults_to_mild(self):
        allergy = Allergy.objects.create(patient=self.patient, name="Penicillin")

        self.assertEqual(allergy.severity, Allergy.SEVERITY_MILD)

    def test_allergy_severity_accepts_all_defined_choices(self):
        for severity, _ in Allergy.SEVERITY_CHOICES:
            allergy = Allergy.objects.create(patient=self.patient, name="Test", severity=severity)
            allergy.full_clean()

            self.assertEqual(allergy.severity, severity)

    def test_allergy_str_representation(self):
        allergy = Allergy.objects.create(
            patient=self.patient, name="Penicillin", severity=Allergy.SEVERITY_MODERATE
        )

        self.assertEqual(str(allergy), "Penicillin - moderate")

    def test_allergy_reverse_access_via_patient(self):
        allergy = Allergy.objects.create(patient=self.patient, name="Penicillin")

        self.assertIn(allergy, self.patient.allergies.all())

    def test_deleting_patient_cascades_to_allergies(self):
        Allergy.objects.create(patient=self.patient, name="Penicillin")

        self.patient.delete()

        self.assertEqual(Allergy.objects.count(), 0)
