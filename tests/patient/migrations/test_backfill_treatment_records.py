"""
Coverage for the data migration `0007_backfill_treatment_records`.

`django-test-migrations` (which would let us execute this against the real
historical migration graph state via `MigratorExecutor`) is not installed in
this environment, so this test imports the migration module directly and
calls its forward/reverse functions against the *current* app registry
(`django.apps.apps`) instead of the historical one produced by
`SchemaEditor`/`migrations.RunPython`. This still exercises the exact
callables Django runs during the migration and the row-shape they produce,
but it does not prove the migration is compatible with the exact model state
of `0006_...` at the point in the graph where it runs. If the models change
further and this migration is edited, this test should be re-pointed at the
historical state (e.g. via `django-test-migrations`) for full fidelity.
"""
import importlib

from django.apps import apps
from django.test import TestCase

from dental_clinic.patient.models import Patient, TreatmentRecord
from dental_clinic.treatment.models import Treatment

migration_module = importlib.import_module(
    'dental_clinic.patient.migrations.0007_backfill_treatment_records'
)


class BackfillTreatmentRecordsMigrationTestCase(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            email="patient@test.com",
            first_name="Firstname",
            last_name="Lastname",
            phone_number="1234567890",
        )
        self.other_patient = Patient.objects.create(
            email="other@test.com",
            first_name="Othername",
            last_name="Otherlast",
            phone_number="0987654321",
        )
        self.treatment = Treatment.objects.create(
            clinical_code="123", name="Filling", cost=100.0, description="Composite filling"
        )
        self.other_treatment = Treatment.objects.create(
            clinical_code="456", name="Cleaning", cost=50.0, description="Routine cleaning"
        )

    def test_backfill_creates_treatment_record_per_legacy_m2m_link(self):
        self.patient.treatment.add(self.treatment, self.other_treatment)
        self.other_patient.treatment.add(self.treatment)

        migration_module.backfill_treatment_records(apps, None)

        self.assertEqual(
            TreatmentRecord.objects.filter(
                patient=self.patient, notes=migration_module.BACKFILL_NOTE
            ).count(),
            2,
        )
        self.assertTrue(
            TreatmentRecord.objects.filter(
                patient=self.patient, treatment=self.treatment, date_performed__isnull=True
            ).exists()
        )
        self.assertTrue(
            TreatmentRecord.objects.filter(
                patient=self.patient, treatment=self.other_treatment, date_performed__isnull=True
            ).exists()
        )
        self.assertTrue(
            TreatmentRecord.objects.filter(
                patient=self.other_patient, treatment=self.treatment
            ).exists()
        )

    def test_backfill_produces_no_records_when_no_legacy_treatments_exist(self):
        migration_module.backfill_treatment_records(apps, None)

        self.assertEqual(TreatmentRecord.objects.count(), 0)

    def test_reverse_migration_removes_only_backfilled_records(self):
        self.patient.treatment.add(self.treatment)
        migration_module.backfill_treatment_records(apps, None)

        manual_record = TreatmentRecord.objects.create(
            patient=self.patient, treatment=self.other_treatment, notes="Manually entered"
        )

        migration_module.remove_backfilled_treatment_records(apps, None)

        self.assertFalse(
            TreatmentRecord.objects.filter(notes=migration_module.BACKFILL_NOTE).exists()
        )
        self.assertTrue(TreatmentRecord.objects.filter(pk=manual_record.pk).exists())
