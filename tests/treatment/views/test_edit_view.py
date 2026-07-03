from django.test import TestCase
from django.urls import reverse
from dental_clinic.auth_app.models import DentistUser
from dental_clinic.treatment.models import Treatment


class TreatmentEditViewTestCase(TestCase):
    def setUp(self):
        self.user = DentistUser.objects.create_user(uin_number='9876543102', password='testpassword')
        self.treatment = Treatment.objects.create(
            clinical_code='123',
            name='Filling',
            cost=100.0,
            description='Composite filling',
            notes='Initial notes',
        )

    def test_treatment_edit_view_unauthenticated_redirects(self):
        url = reverse('treatment-edit', args=[self.treatment.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/authentication/login/?next=' + url)

    def test_treatment_edit_view_authenticated_get_renders_template(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('treatment-edit', args=[self.treatment.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/treatment/edit-treatment.html')

    def test_treatment_edit_view_authenticated_post_with_notes_updates_treatment(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('treatment-edit', args=[self.treatment.pk])

        form_data = {
            'clinical_code': '789',
            'name': 'Root canal',
            'cost': 300.0,
            'description': 'Root canal therapy',
            'notes': 'Updated notes',
        }
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('appointments-catalogue'))
        self.treatment.refresh_from_db()
        self.assertEqual(self.treatment.clinical_code, '789')
        self.assertEqual(self.treatment.name, 'Root canal')
        self.assertEqual(self.treatment.notes, 'Updated notes')

    def test_treatment_edit_view_authenticated_post_without_notes_clears_notes(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('treatment-edit', args=[self.treatment.pk])

        form_data = {
            'clinical_code': '321',
            'name': 'Cleaning',
            'cost': 50.0,
            'description': 'Routine cleaning',
        }
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('appointments-catalogue'))
        self.treatment.refresh_from_db()
        self.assertEqual(self.treatment.notes, '')
