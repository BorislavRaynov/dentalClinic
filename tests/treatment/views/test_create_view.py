from django.test import TestCase
from django.urls import reverse
from dental_clinic.auth_app.models import DentistUser
from dental_clinic.treatment.models import Treatment


class TreatmentCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = DentistUser.objects.create_user(uin_number='9876543102', password='testpassword')

    def test_treatment_create_view_unauthenticated_redirects(self):
        url = reverse('treatment-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/authentication/login/?next=' + url)

    def test_treatment_create_view_authenticated_get_renders_template(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('treatment-create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/treatment/create-treatment.html')

    def test_treatment_create_view_authenticated_post_with_notes_creates_treatment(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('treatment-create')

        form_data = {
            'clinical_code': '123',
            'name': 'Filling',
            'cost': 100.0,
            'description': 'Composite filling',
            'notes': 'Patient allergic to latex',
        }
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('appointments-catalogue'))
        treatment = Treatment.objects.get(clinical_code='123')
        self.assertEqual(treatment.notes, 'Patient allergic to latex')

    def test_treatment_create_view_authenticated_post_without_notes_creates_treatment(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('treatment-create')

        form_data = {
            'clinical_code': '456',
            'name': 'Extraction',
            'cost': 200.0,
            'description': 'Tooth extraction',
        }
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('appointments-catalogue'))
        treatment = Treatment.objects.get(clinical_code='456')
        self.assertEqual(treatment.notes, '')
