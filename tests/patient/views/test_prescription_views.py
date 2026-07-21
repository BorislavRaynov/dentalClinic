from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from dental_clinic.auth_app.models import DentistUser
from dental_clinic.patient.models import Patient, Prescription


class PrescriptionCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = DentistUser.objects.create_user(uin_number='9876543102', password='testpassword')
        self.patient = Patient.objects.create(
            email="patient@test.com",
            first_name="Firstname",
            last_name="Lastname",
            phone_number="1234567890",
        )

    def test_prescription_create_view_unauthenticated_redirects(self):
        url = reverse('prescription-add', args=[self.patient.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '/authentication/login/?next=' + url, fetch_redirect_response=False
        )

    def test_prescription_create_view_authenticated_get_renders_template(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('prescription-add', args=[self.patient.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/add-prescription.html')

    def test_prescription_create_view_authenticated_post_sets_patient_and_prescriber_and_redirects(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('prescription-add', args=[self.patient.pk])
        form_data = {
            'medication': 'Amoxicillin',
            'dosage': '500mg',
            'instructions': 'Take three times daily',
            'date_prescribed': timezone.localdate().isoformat(),
        }
        response = self.client.post(url, data=form_data)

        self.assertRedirects(
            response,
            reverse('patient-medical-record', args=[self.patient.pk]),
            fetch_redirect_response=False,
        )
        prescription = Prescription.objects.get(medication='Amoxicillin')
        self.assertEqual(prescription.patient_id, self.patient.pk)
        self.assertEqual(prescription.prescribed_by_id, self.user.pk)

    def test_prescription_create_view_authenticated_post_missing_required_medication_reruns_form(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('prescription-add', args=[self.patient.pk])
        form_data = {
            'dosage': '500mg',
            'date_prescribed': timezone.localdate().isoformat(),
        }
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/add-prescription.html')
        self.assertFalse(Prescription.objects.filter(patient=self.patient).exists())

    def test_prescription_create_view_authenticated_post_future_date_prescribed_reruns_form(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('prescription-add', args=[self.patient.pk])
        future_date = timezone.localdate() + timedelta(days=1)
        form_data = {
            'medication': 'Amoxicillin',
            'dosage': '500mg',
            'date_prescribed': future_date.isoformat(),
        }
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/add-prescription.html')
        self.assertFalse(Prescription.objects.filter(patient=self.patient).exists())


class PrescriptionUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = DentistUser.objects.create_user(uin_number='9876543102', password='testpassword')
        self.patient = Patient.objects.create(
            email="patient@test.com",
            first_name="Firstname",
            last_name="Lastname",
            phone_number="1234567890",
        )
        self.prescription = Prescription.objects.create(
            patient=self.patient, prescribed_by=self.user, medication="Amoxicillin", dosage="500mg"
        )

    def test_prescription_edit_view_unauthenticated_redirects(self):
        url = reverse('prescription-edit', args=[self.prescription.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '/authentication/login/?next=' + url, fetch_redirect_response=False
        )

    def test_prescription_edit_view_authenticated_get_renders_template(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('prescription-edit', args=[self.prescription.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/edit-prescription.html')

    def test_prescription_edit_view_authenticated_post_persists_changes(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('prescription-edit', args=[self.prescription.pk])
        form_data = {
            'medication': 'Ibuprofen',
            'dosage': '200mg',
            'date_prescribed': timezone.localdate().isoformat(),
        }
        response = self.client.post(url, data=form_data)

        self.assertRedirects(
            response,
            reverse('patient-medical-record', args=[self.patient.pk]),
            fetch_redirect_response=False,
        )
        self.prescription.refresh_from_db()
        self.assertEqual(self.prescription.medication, 'Ibuprofen')
        self.assertEqual(self.prescription.dosage, '200mg')

    def test_prescription_edit_view_authenticated_post_missing_required_medication_reruns_form(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('prescription-edit', args=[self.prescription.pk])
        form_data = {
            'dosage': '200mg',
            'date_prescribed': timezone.localdate().isoformat(),
        }
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/edit-prescription.html')
        self.prescription.refresh_from_db()
        self.assertEqual(self.prescription.medication, 'Amoxicillin')


class PrescriptionDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = DentistUser.objects.create_user(uin_number='9876543102', password='testpassword')
        self.patient = Patient.objects.create(
            email="patient@test.com",
            first_name="Firstname",
            last_name="Lastname",
            phone_number="1234567890",
        )
        self.prescription = Prescription.objects.create(
            patient=self.patient, prescribed_by=self.user, medication="Amoxicillin", dosage="500mg"
        )

    def test_prescription_delete_view_unauthenticated_redirects(self):
        url = reverse('prescription-delete', args=[self.prescription.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '/authentication/login/?next=' + url, fetch_redirect_response=False
        )

    def test_prescription_delete_view_authenticated_get_renders_template(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('prescription-delete', args=[self.prescription.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/delete-prescription.html')

    def test_prescription_delete_view_authenticated_post_removes_prescription(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('prescription-delete', args=[self.prescription.pk])
        response = self.client.post(url)

        self.assertRedirects(
            response,
            reverse('patient-medical-record', args=[self.patient.pk]),
            fetch_redirect_response=False,
        )
        self.assertFalse(Prescription.objects.filter(pk=self.prescription.pk).exists())
