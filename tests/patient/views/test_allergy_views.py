from django.test import TestCase
from django.urls import reverse

from dental_clinic.auth_app.models import DentistUser
from dental_clinic.patient.models import Allergy, Patient


class AllergyCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = DentistUser.objects.create_user(uin_number='9876543102', password='testpassword')
        self.patient = Patient.objects.create(
            email="patient@test.com",
            first_name="Firstname",
            last_name="Lastname",
            phone_number="1234567890",
        )

    def test_allergy_create_view_unauthenticated_redirects(self):
        url = reverse('allergy-add', args=[self.patient.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '/authentication/login/?next=' + url, fetch_redirect_response=False
        )

    def test_allergy_create_view_authenticated_get_renders_template(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('allergy-add', args=[self.patient.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/add-allergy.html')

    def test_allergy_create_view_authenticated_post_sets_patient_from_url_and_redirects(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('allergy-add', args=[self.patient.pk])
        form_data = {'name': 'Penicillin', 'severity': Allergy.SEVERITY_SEVERE, 'reaction': 'Rash'}
        response = self.client.post(url, data=form_data)

        self.assertRedirects(
            response,
            reverse('patient-medical-record', args=[self.patient.pk]),
            fetch_redirect_response=False,
        )
        allergy = Allergy.objects.get(name='Penicillin')
        self.assertEqual(allergy.patient_id, self.patient.pk)

    def test_allergy_create_view_authenticated_post_missing_required_name_reruns_form(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('allergy-add', args=[self.patient.pk])
        form_data = {'severity': Allergy.SEVERITY_SEVERE, 'reaction': 'Rash'}
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/add-allergy.html')
        self.assertFalse(Allergy.objects.filter(patient=self.patient).exists())


class AllergyUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = DentistUser.objects.create_user(uin_number='9876543102', password='testpassword')
        self.patient = Patient.objects.create(
            email="patient@test.com",
            first_name="Firstname",
            last_name="Lastname",
            phone_number="1234567890",
        )
        self.allergy = Allergy.objects.create(patient=self.patient, name="Penicillin")

    def test_allergy_edit_view_unauthenticated_redirects(self):
        url = reverse('allergy-edit', args=[self.allergy.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '/authentication/login/?next=' + url, fetch_redirect_response=False
        )

    def test_allergy_edit_view_authenticated_get_renders_template(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('allergy-edit', args=[self.allergy.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/edit-allergy.html')

    def test_allergy_edit_view_authenticated_post_persists_changes(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('allergy-edit', args=[self.allergy.pk])
        form_data = {'name': 'Latex', 'severity': Allergy.SEVERITY_MODERATE, 'reaction': 'Hives'}
        response = self.client.post(url, data=form_data)

        self.assertRedirects(
            response,
            reverse('patient-medical-record', args=[self.patient.pk]),
            fetch_redirect_response=False,
        )
        self.allergy.refresh_from_db()
        self.assertEqual(self.allergy.name, 'Latex')
        self.assertEqual(self.allergy.severity, Allergy.SEVERITY_MODERATE)
        self.assertEqual(self.allergy.reaction, 'Hives')

    def test_allergy_edit_view_authenticated_post_missing_required_name_reruns_form(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('allergy-edit', args=[self.allergy.pk])
        form_data = {'severity': Allergy.SEVERITY_MODERATE}
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/edit-allergy.html')
        self.allergy.refresh_from_db()
        self.assertEqual(self.allergy.name, 'Penicillin')


class AllergyDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = DentistUser.objects.create_user(uin_number='9876543102', password='testpassword')
        self.patient = Patient.objects.create(
            email="patient@test.com",
            first_name="Firstname",
            last_name="Lastname",
            phone_number="1234567890",
        )
        self.allergy = Allergy.objects.create(patient=self.patient, name="Penicillin")

    def test_allergy_delete_view_unauthenticated_redirects(self):
        url = reverse('allergy-delete', args=[self.allergy.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '/authentication/login/?next=' + url, fetch_redirect_response=False
        )

    def test_allergy_delete_view_authenticated_get_renders_template(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('allergy-delete', args=[self.allergy.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/delete-allergy.html')

    def test_allergy_delete_view_authenticated_post_removes_allergy(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('allergy-delete', args=[self.allergy.pk])
        response = self.client.post(url)

        self.assertRedirects(
            response,
            reverse('patient-medical-record', args=[self.patient.pk]),
            fetch_redirect_response=False,
        )
        self.assertFalse(Allergy.objects.filter(pk=self.allergy.pk).exists())
