from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from dental_clinic.auth_app.models import DentistUser
from dental_clinic.patient.models import MedicalHistoryEntry, Patient


class MedicalHistoryEntryCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = DentistUser.objects.create_user(uin_number='9876543102', password='testpassword')
        self.patient = Patient.objects.create(
            email="patient@test.com",
            first_name="Firstname",
            last_name="Lastname",
            phone_number="1234567890",
        )

    def test_history_create_view_unauthenticated_redirects(self):
        url = reverse('history-add', args=[self.patient.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '/authentication/login/?next=' + url, fetch_redirect_response=False
        )

    def test_history_create_view_authenticated_get_renders_template(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('history-add', args=[self.patient.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/add-history-entry.html')

    def test_history_create_view_authenticated_post_sets_patient_from_url_and_redirects(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('history-add', args=[self.patient.pk])
        form_data = {
            'entry_date': timezone.localdate().isoformat(),
            'note': 'Routine checkup',
        }
        response = self.client.post(url, data=form_data)

        self.assertRedirects(
            response,
            reverse('patient-medical-record', args=[self.patient.pk]),
            fetch_redirect_response=False,
        )
        entry = MedicalHistoryEntry.objects.get(note='Routine checkup')
        self.assertEqual(entry.patient_id, self.patient.pk)

    def test_history_create_view_authenticated_post_missing_required_note_reruns_form(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('history-add', args=[self.patient.pk])
        form_data = {'entry_date': timezone.localdate().isoformat()}
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/add-history-entry.html')
        self.assertFalse(MedicalHistoryEntry.objects.filter(patient=self.patient).exists())

    def test_history_create_view_authenticated_post_future_entry_date_reruns_form(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('history-add', args=[self.patient.pk])
        future_date = timezone.localdate() + timedelta(days=1)
        form_data = {'entry_date': future_date.isoformat(), 'note': 'Future note'}
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/add-history-entry.html')
        self.assertFalse(MedicalHistoryEntry.objects.filter(patient=self.patient).exists())


class MedicalHistoryEntryUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = DentistUser.objects.create_user(uin_number='9876543102', password='testpassword')
        self.patient = Patient.objects.create(
            email="patient@test.com",
            first_name="Firstname",
            last_name="Lastname",
            phone_number="1234567890",
        )
        self.entry = MedicalHistoryEntry.objects.create(patient=self.patient, note="Routine checkup")

    def test_history_edit_view_unauthenticated_redirects(self):
        url = reverse('history-edit', args=[self.entry.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '/authentication/login/?next=' + url, fetch_redirect_response=False
        )

    def test_history_edit_view_authenticated_get_renders_template(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('history-edit', args=[self.entry.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/edit-history-entry.html')

    def test_history_edit_view_authenticated_post_persists_changes(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('history-edit', args=[self.entry.pk])
        earlier_date = timezone.localdate() - timedelta(days=2)
        form_data = {
            'entry_date': earlier_date.isoformat(),
            'note': 'Follow-up visit',
        }
        response = self.client.post(url, data=form_data)

        self.assertRedirects(
            response,
            reverse('patient-medical-record', args=[self.patient.pk]),
            fetch_redirect_response=False,
        )
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.note, 'Follow-up visit')
        self.assertEqual(self.entry.entry_date, earlier_date)

    def test_history_edit_view_authenticated_post_missing_required_note_reruns_form(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('history-edit', args=[self.entry.pk])
        form_data = {'entry_date': timezone.localdate().isoformat()}
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/edit-history-entry.html')
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.note, 'Routine checkup')


class MedicalHistoryEntryDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = DentistUser.objects.create_user(uin_number='9876543102', password='testpassword')
        self.patient = Patient.objects.create(
            email="patient@test.com",
            first_name="Firstname",
            last_name="Lastname",
            phone_number="1234567890",
        )
        self.entry = MedicalHistoryEntry.objects.create(patient=self.patient, note="Routine checkup")

    def test_history_delete_view_unauthenticated_redirects(self):
        url = reverse('history-delete', args=[self.entry.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '/authentication/login/?next=' + url, fetch_redirect_response=False
        )

    def test_history_delete_view_authenticated_get_renders_template(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('history-delete', args=[self.entry.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/delete-history-entry.html')

    def test_history_delete_view_authenticated_post_removes_entry(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('history-delete', args=[self.entry.pk])
        response = self.client.post(url)

        self.assertRedirects(
            response,
            reverse('patient-medical-record', args=[self.patient.pk]),
            fetch_redirect_response=False,
        )
        self.assertFalse(MedicalHistoryEntry.objects.filter(pk=self.entry.pk).exists())
