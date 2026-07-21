from django.test import TestCase
from django.urls import reverse

from dental_clinic.auth_app.models import DentistUser
from dental_clinic.patient.models import ClinicalNote, Patient


class ClinicalNoteCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = DentistUser.objects.create_user(uin_number='9876543102', password='testpassword')
        self.patient = Patient.objects.create(
            email="patient@test.com",
            first_name="Firstname",
            last_name="Lastname",
            phone_number="1234567890",
        )

    def test_note_create_view_unauthenticated_redirects(self):
        url = reverse('note-add', args=[self.patient.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '/authentication/login/?next=' + url, fetch_redirect_response=False
        )

    def test_note_create_view_authenticated_get_renders_template(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('note-add', args=[self.patient.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/add-note.html')

    def test_note_create_view_authenticated_post_sets_patient_and_author_and_redirects(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('note-add', args=[self.patient.pk])
        form_data = {'body': 'Patient reports mild pain.'}
        response = self.client.post(url, data=form_data)

        self.assertRedirects(
            response,
            reverse('patient-medical-record', args=[self.patient.pk]),
            fetch_redirect_response=False,
        )
        note = ClinicalNote.objects.get(body='Patient reports mild pain.')
        self.assertEqual(note.patient_id, self.patient.pk)
        self.assertEqual(note.author_id, self.user.pk)

    def test_note_create_view_authenticated_post_missing_required_body_reruns_form(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('note-add', args=[self.patient.pk])
        response = self.client.post(url, data={})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/add-note.html')
        self.assertFalse(ClinicalNote.objects.filter(patient=self.patient).exists())


class ClinicalNoteUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = DentistUser.objects.create_user(uin_number='9876543102', password='testpassword')
        self.patient = Patient.objects.create(
            email="patient@test.com",
            first_name="Firstname",
            last_name="Lastname",
            phone_number="1234567890",
        )
        self.note = ClinicalNote.objects.create(
            patient=self.patient, author=self.user, body="Initial note"
        )

    def test_note_edit_view_unauthenticated_redirects(self):
        url = reverse('note-edit', args=[self.note.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '/authentication/login/?next=' + url, fetch_redirect_response=False
        )

    def test_note_edit_view_authenticated_get_renders_template(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('note-edit', args=[self.note.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/edit-note.html')

    def test_note_edit_view_authenticated_post_persists_changes(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('note-edit', args=[self.note.pk])
        form_data = {'body': 'Updated note body'}
        response = self.client.post(url, data=form_data)

        self.assertRedirects(
            response,
            reverse('patient-medical-record', args=[self.patient.pk]),
            fetch_redirect_response=False,
        )
        self.note.refresh_from_db()
        self.assertEqual(self.note.body, 'Updated note body')

    def test_note_edit_view_authenticated_post_missing_required_body_reruns_form(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('note-edit', args=[self.note.pk])
        response = self.client.post(url, data={})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/edit-note.html')
        self.note.refresh_from_db()
        self.assertEqual(self.note.body, 'Initial note')


class ClinicalNoteDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = DentistUser.objects.create_user(uin_number='9876543102', password='testpassword')
        self.patient = Patient.objects.create(
            email="patient@test.com",
            first_name="Firstname",
            last_name="Lastname",
            phone_number="1234567890",
        )
        self.note = ClinicalNote.objects.create(
            patient=self.patient, author=self.user, body="Initial note"
        )

    def test_note_delete_view_unauthenticated_redirects(self):
        url = reverse('note-delete', args=[self.note.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '/authentication/login/?next=' + url, fetch_redirect_response=False
        )

    def test_note_delete_view_authenticated_get_renders_template(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('note-delete', args=[self.note.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/delete-note.html')

    def test_note_delete_view_authenticated_post_removes_note(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('note-delete', args=[self.note.pk])
        response = self.client.post(url)

        self.assertRedirects(
            response,
            reverse('patient-medical-record', args=[self.patient.pk]),
            fetch_redirect_response=False,
        )
        self.assertFalse(ClinicalNote.objects.filter(pk=self.note.pk).exists())
