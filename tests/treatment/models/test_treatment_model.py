from django.test import TestCase
from dental_clinic.treatment.models import Treatment


class TreatmentModelTestCase(TestCase):

    VALID_TREATMENT_DATA = {
        "clinical_code": "123",
        "name": "Filling",
        "cost": 100.0,
        "description": "Composite filling",
    }

    def test_create_treatment_without_notes_defaults_to_empty_string(self):
        treatment = Treatment.objects.create(**self.VALID_TREATMENT_DATA)
        treatment.full_clean()

        self.assertEqual(treatment.notes, '')
        self.assertEqual(treatment.clinical_code, "123")
        self.assertEqual(treatment.name, "Filling")
        self.assertEqual(treatment.cost, 100.0)
        self.assertEqual(treatment.description, "Composite filling")

    def test_create_treatment_with_notes_persists_value(self):
        treatment = Treatment.objects.create(
            notes="Patient allergic to latex",
            **self.VALID_TREATMENT_DATA
        )
        treatment.full_clean()
        treatment.refresh_from_db()

        self.assertEqual(treatment.notes, "Patient allergic to latex")

    def test_treatment_notes_blank_is_valid_on_full_clean(self):
        treatment = Treatment(**self.VALID_TREATMENT_DATA)

        treatment.full_clean()
