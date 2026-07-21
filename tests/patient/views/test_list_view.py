from django.test import TestCase
from django.urls import reverse

from dental_clinic.auth_app.models import DentistUser
from dental_clinic.patient.models import Patient


class PatientListViewSearchTestCase(TestCase):
    def setUp(self):
        self.user = DentistUser.objects.create_user(uin_number='9876543102', password='testpassword')
        self.client.login(uin_number='9876543102', password='testpassword')
        self.patient1 = Patient.objects.create(
            email="john.doe@test.com",
            first_name="John",
            last_name="Doe",
            phone_number="1234567890",
        )
        self.patient2 = Patient.objects.create(
            email="jane.roe@test.com",
            first_name="Jane",
            last_name="Roe",
            phone_number="0987654321",
        )

    def test_patient_list_view_unauthenticated_redirects(self):
        self.client.logout()
        url = reverse('patients-catalogue')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '/authentication/login/?next=' + url, fetch_redirect_response=False
        )

    def test_search_matches_by_last_name(self):
        url = reverse('patients-catalogue')
        response = self.client.get(url, {'search': 'Doe'})

        self.assertEqual(list(response.context['object_list']), [self.patient1])

    def test_search_matches_by_first_name(self):
        url = reverse('patients-catalogue')
        response = self.client.get(url, {'search': 'Jane'})

        self.assertEqual(list(response.context['object_list']), [self.patient2])

    def test_search_matches_by_patient_id(self):
        url = reverse('patients-catalogue')
        response = self.client.get(url, {'search': self.patient1.patient_id})

        self.assertEqual(list(response.context['object_list']), [self.patient1])

    def test_search_matches_by_email(self):
        url = reverse('patients-catalogue')
        response = self.client.get(url, {'search': 'jane.roe'})

        self.assertEqual(list(response.context['object_list']), [self.patient2])

    def test_search_matches_by_phone_number(self):
        url = reverse('patients-catalogue')
        response = self.client.get(url, {'search': '0987654321'})

        self.assertEqual(list(response.context['object_list']), [self.patient2])

    def test_search_with_no_match_returns_empty(self):
        url = reverse('patients-catalogue')
        response = self.client.get(url, {'search': 'Nonexistent'})

        self.assertEqual(list(response.context['object_list']), [])

    def test_search_without_query_returns_all_patients(self):
        url = reverse('patients-catalogue')
        response = self.client.get(url)

        self.assertEqual(len(response.context['object_list']), 2)
