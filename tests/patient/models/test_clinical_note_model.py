from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from dental_clinic.auth_app.models import DentistUser
from dental_clinic.patient.models import ClinicalNote, Patient


class ClinicalNoteModelTestCase(TestCase):

    def setUp(self):
        self.patient = Patient.objects.create(
            email="patient@test.com",
            first_name="Firstname",
            last_name="Lastname",
            phone_number="1234567890",
        )
        self.author = DentistUser.objects.create_user(
            uin_number='9876543102', password='testpassword'
        )

    def test_create_clinical_note_with_valid_data(self):
        note = ClinicalNote.objects.create(
            patient=self.patient, author=self.author, body="Patient reports mild pain."
        )
        note.full_clean()

        self.assertEqual(note.body, "Patient reports mild pain.")
        self.assertEqual(note.patient, self.patient)
        self.assertEqual(note.author, self.author)

    def test_clinical_note_created_at_defaults_to_now(self):
        before = timezone.now()
        note = ClinicalNote.objects.create(patient=self.patient, body="Note body")
        after = timezone.now()

        self.assertTrue(before <= note.created_at <= after)

    def test_clinical_note_created_at_is_not_editable(self):
        field = ClinicalNote._meta.get_field('created_at')

        self.assertFalse(field.editable)

    def test_clinical_notes_ordered_by_created_at_descending(self):
        older = ClinicalNote.objects.create(
            patient=self.patient,
            body="Older note",
            created_at=timezone.now() - timedelta(days=1),
        )
        newer = ClinicalNote.objects.create(
            patient=self.patient, body="Newer note", created_at=timezone.now()
        )

        notes = list(ClinicalNote.objects.all())

        self.assertEqual(notes, [newer, older])

    def test_clinical_note_str_representation(self):
        note = ClinicalNote.objects.create(patient=self.patient, body="Note body")

        self.assertEqual(str(note), f"{self.patient} note {note.created_at:%Y-%m-%d}")

    def test_clinical_note_reverse_access_via_patient(self):
        note = ClinicalNote.objects.create(patient=self.patient, body="Note body")

        self.assertIn(note, self.patient.clinical_notes.all())

    def test_deleting_patient_cascades_to_clinical_notes(self):
        ClinicalNote.objects.create(patient=self.patient, body="Note body")

        self.patient.delete()

        self.assertEqual(ClinicalNote.objects.count(), 0)

    def test_deleting_author_sets_null_on_clinical_note(self):
        note = ClinicalNote.objects.create(
            patient=self.patient, author=self.author, body="Note body"
        )

        self.author.delete()
        note.refresh_from_db()

        self.assertIsNone(note.author)
