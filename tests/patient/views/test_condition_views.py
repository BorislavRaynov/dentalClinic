from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from dental_clinic.auth_app.models import DentistUser
from dental_clinic.patient.models import MedicalCondition, Patient


class MedicalConditionCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = DentistUser.objects.create_user(uin_number='9876543102', password='testpassword')
        self.patient = Patient.objects.create(
            email="patient@test.com",
            first_name="Firstname",
            last_name="Lastname",
            phone_number="1234567890",
        )

    def test_condition_create_view_unauthenticated_redirects(self):
        url = reverse('condition-add', args=[self.patient.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '/authentication/login/?next=' + url, fetch_redirect_response=False
        )

    def test_condition_create_view_authenticated_get_renders_template(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('condition-add', args=[self.patient.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/add-condition.html')

    def test_condition_create_view_authenticated_post_sets_patient_from_url_and_redirects(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('condition-add', args=[self.patient.pk])
        form_data = {'name': 'Diabetes', 'status': MedicalCondition.STATUS_ACTIVE}
        response = self.client.post(url, data=form_data)

        self.assertRedirects(
            response,
            reverse('patient-medical-record', args=[self.patient.pk]),
            fetch_redirect_response=False,
        )
        condition = MedicalCondition.objects.get(name='Diabetes')
        self.assertEqual(condition.patient_id, self.patient.pk)

    def test_condition_create_view_authenticated_post_missing_required_name_reruns_form(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('condition-add', args=[self.patient.pk])
        form_data = {'status': MedicalCondition.STATUS_ACTIVE}
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/add-condition.html')
        self.assertFalse(MedicalCondition.objects.filter(patient=self.patient).exists())

    def test_condition_create_view_authenticated_post_future_diagnosed_date_reruns_form(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('condition-add', args=[self.patient.pk])
        future_date = timezone.localdate() + timedelta(days=1)
        form_data = {
            'name': 'Diabetes',
            'status': MedicalCondition.STATUS_ACTIVE,
            'diagnosed_date': future_date.isoformat(),
        }
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/add-condition.html')
        self.assertFalse(MedicalCondition.objects.filter(patient=self.patient).exists())


class MedicalConditionUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = DentistUser.objects.create_user(uin_number='9876543102', password='testpassword')
        self.patient = Patient.objects.create(
            email="patient@test.com",
            first_name="Firstname",
            last_name="Lastname",
            phone_number="1234567890",
        )
        self.condition = MedicalCondition.objects.create(patient=self.patient, name="Diabetes")

    def test_condition_edit_view_unauthenticated_redirects(self):
        url = reverse('condition-edit', args=[self.condition.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '/authentication/login/?next=' + url, fetch_redirect_response=False
        )

    def test_condition_edit_view_authenticated_get_renders_template(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('condition-edit', args=[self.condition.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/edit-condition.html')

    def test_condition_edit_view_authenticated_post_persists_changes(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('condition-edit', args=[self.condition.pk])
        form_data = {'name': 'Hypertension', 'status': MedicalCondition.STATUS_RESOLVED}
        response = self.client.post(url, data=form_data)

        self.assertRedirects(
            response,
            reverse('patient-medical-record', args=[self.patient.pk]),
            fetch_redirect_response=False,
        )
        self.condition.refresh_from_db()
        self.assertEqual(self.condition.name, 'Hypertension')
        self.assertEqual(self.condition.status, MedicalCondition.STATUS_RESOLVED)

    def test_condition_edit_view_authenticated_post_missing_required_name_reruns_form(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('condition-edit', args=[self.condition.pk])
        form_data = {'status': MedicalCondition.STATUS_RESOLVED}
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/edit-condition.html')
        self.condition.refresh_from_db()
        self.assertEqual(self.condition.name, 'Diabetes')


class MedicalConditionDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = DentistUser.objects.create_user(uin_number='9876543102', password='testpassword')
        self.patient = Patient.objects.create(
            email="patient@test.com",
            first_name="Firstname",
            last_name="Lastname",
            phone_number="1234567890",
        )
        self.condition = MedicalCondition.objects.create(patient=self.patient, name="Diabetes")

    def test_condition_delete_view_unauthenticated_redirects(self):
        url = reverse('condition-delete', args=[self.condition.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '/authentication/login/?next=' + url, fetch_redirect_response=False
        )

    def test_condition_delete_view_authenticated_get_renders_template(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('condition-delete', args=[self.condition.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/delete-condition.html')

    def test_condition_delete_view_authenticated_post_removes_condition(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('condition-delete', args=[self.condition.pk])
        response = self.client.post(url)

        self.assertRedirects(
            response,
            reverse('patient-medical-record', args=[self.patient.pk]),
            fetch_redirect_response=False,
        )
        self.assertFalse(MedicalCondition.objects.filter(pk=self.condition.pk).exists())
