from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from dental_clinic.appointment.models import Appointment
from dental_clinic.auth_app.models import DentistUser
from dental_clinic.patient.models import Patient, TreatmentRecord
from dental_clinic.treatment.models import Treatment


class TreatmentRecordCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = DentistUser.objects.create_user(uin_number='9876543102', password='testpassword')
        self.patient = Patient.objects.create(
            email="patient@test.com",
            first_name="Firstname",
            last_name="Lastname",
            phone_number="1234567890",
        )
        self.treatment = Treatment.objects.create(
            clinical_code="123",
            name="Filling",
            cost=100.0,
            description="Composite filling",
        )
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            dentist=self.user,
            date=timezone.localdate(),
            time="10:00:00",
        )

    def test_treatment_record_create_view_unauthenticated_redirects(self):
        url = reverse('treatment-record-add', args=[self.patient.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '/authentication/login/?next=' + url, fetch_redirect_response=False
        )

    def test_treatment_record_create_view_authenticated_get_renders_template(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('treatment-record-add', args=[self.patient.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/add-treatment-record.html')

    def test_treatment_record_create_view_authenticated_post_sets_patient_and_performer_and_redirects(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('treatment-record-add', args=[self.patient.pk])
        form_data = {
            'treatment': self.treatment.pk,
            'appointment': self.appointment.pk,
            'date_performed': timezone.localdate().isoformat(),
            'tooth': '14',
            'notes': 'Straightforward filling',
        }
        response = self.client.post(url, data=form_data)

        self.assertRedirects(
            response,
            reverse('patient-medical-record', args=[self.patient.pk]),
            fetch_redirect_response=False,
        )
        record = TreatmentRecord.objects.get(tooth='14')
        self.assertEqual(record.patient_id, self.patient.pk)
        self.assertEqual(record.performed_by_id, self.user.pk)
        self.assertEqual(record.treatment_id, self.treatment.pk)

    def test_treatment_record_create_view_authenticated_post_missing_required_treatment_reruns_form(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('treatment-record-add', args=[self.patient.pk])
        form_data = {
            'date_performed': timezone.localdate().isoformat(),
            'tooth': '14',
        }
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/add-treatment-record.html')
        self.assertFalse(TreatmentRecord.objects.filter(patient=self.patient).exists())

    def test_treatment_record_create_view_authenticated_post_future_date_performed_reruns_form(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('treatment-record-add', args=[self.patient.pk])
        future_date = timezone.localdate() + timedelta(days=1)
        form_data = {
            'treatment': self.treatment.pk,
            'date_performed': future_date.isoformat(),
        }
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/add-treatment-record.html')
        self.assertFalse(TreatmentRecord.objects.filter(patient=self.patient).exists())

    def test_treatment_record_create_view_appointment_field_scoped_to_patient(self):
        other_patient = Patient.objects.create(
            email="other@test.com",
            first_name="Othername",
            last_name="Otherlast",
            phone_number="0987654321",
        )
        other_appointment = Appointment.objects.create(
            patient=other_patient,
            dentist=self.user,
            date=timezone.localdate(),
            time="11:00:00",
        )
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('treatment-record-add', args=[self.patient.pk])
        response = self.client.get(url)

        appointment_queryset = response.context['form'].fields['appointment'].queryset
        self.assertIn(self.appointment, appointment_queryset)
        self.assertNotIn(other_appointment, appointment_queryset)


class TreatmentRecordUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = DentistUser.objects.create_user(uin_number='9876543102', password='testpassword')
        self.patient = Patient.objects.create(
            email="patient@test.com",
            first_name="Firstname",
            last_name="Lastname",
            phone_number="1234567890",
        )
        self.treatment = Treatment.objects.create(
            clinical_code="123",
            name="Filling",
            cost=100.0,
            description="Composite filling",
        )
        self.record = TreatmentRecord.objects.create(
            patient=self.patient,
            treatment=self.treatment,
            performed_by=self.user,
            tooth="14",
        )

    def test_treatment_record_edit_view_unauthenticated_redirects(self):
        url = reverse('treatment-record-edit', args=[self.record.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '/authentication/login/?next=' + url, fetch_redirect_response=False
        )

    def test_treatment_record_edit_view_authenticated_get_renders_template(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('treatment-record-edit', args=[self.record.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/edit-treatment-record.html')

    def test_treatment_record_edit_view_authenticated_post_persists_changes(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('treatment-record-edit', args=[self.record.pk])
        form_data = {
            'treatment': self.treatment.pk,
            'date_performed': timezone.localdate().isoformat(),
            'tooth': '15',
            'notes': 'Follow-up filling',
        }
        response = self.client.post(url, data=form_data)

        self.assertRedirects(
            response,
            reverse('patient-medical-record', args=[self.patient.pk]),
            fetch_redirect_response=False,
        )
        self.record.refresh_from_db()
        self.assertEqual(self.record.tooth, '15')
        self.assertEqual(self.record.notes, 'Follow-up filling')

    def test_treatment_record_edit_view_authenticated_post_missing_required_treatment_reruns_form(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('treatment-record-edit', args=[self.record.pk])
        form_data = {'tooth': '15'}
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/edit-treatment-record.html')
        self.record.refresh_from_db()
        self.assertEqual(self.record.tooth, '14')


class TreatmentRecordDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = DentistUser.objects.create_user(uin_number='9876543102', password='testpassword')
        self.patient = Patient.objects.create(
            email="patient@test.com",
            first_name="Firstname",
            last_name="Lastname",
            phone_number="1234567890",
        )
        self.treatment = Treatment.objects.create(
            clinical_code="123",
            name="Filling",
            cost=100.0,
            description="Composite filling",
        )
        self.record = TreatmentRecord.objects.create(
            patient=self.patient, treatment=self.treatment, performed_by=self.user
        )

    def test_treatment_record_delete_view_unauthenticated_redirects(self):
        url = reverse('treatment-record-delete', args=[self.record.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '/authentication/login/?next=' + url, fetch_redirect_response=False
        )

    def test_treatment_record_delete_view_authenticated_get_renders_template(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('treatment-record-delete', args=[self.record.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/delete-treatment-record.html')

    def test_treatment_record_delete_view_authenticated_post_removes_record(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('treatment-record-delete', args=[self.record.pk])
        response = self.client.post(url)

        self.assertRedirects(
            response,
            reverse('patient-medical-record', args=[self.patient.pk]),
            fetch_redirect_response=False,
        )
        self.assertFalse(TreatmentRecord.objects.filter(pk=self.record.pk).exists())
