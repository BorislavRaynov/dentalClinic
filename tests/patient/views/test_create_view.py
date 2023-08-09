from django.test import TestCase
from django.urls import reverse
from dental_clinic.auth_app.models import DentistUser
from dental_clinic.patient.models import Patient


class PatientCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = DentistUser.objects.create_user(uin_number='9876543102', password='testpassword')

    def test_patient_create_view_authenticated_succeessful(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('create-patient')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/create-patient.html')

        form_data = {
            'email': 'newpatient@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '1234567890'
        }
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('appointment-create'))
        self.assertTrue(Patient.objects.filter(email='newpatient@example.com').exists())

    def test_patient_create_view_unauthenticated_redirects(self):
        url = reverse('create-patient')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/authentication/login/?next=' + url)
