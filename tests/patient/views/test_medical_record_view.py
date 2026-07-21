from django.test import TestCase
from django.urls import reverse

from dental_clinic.auth_app.models import DentistUser
from dental_clinic.patient.models import (
    Allergy,
    ClinicalNote,
    MedicalCondition,
    MedicalHistoryEntry,
    Patient,
    Prescription,
    TreatmentRecord,
)
from dental_clinic.patient.views import PatientMedicalRecordView
from dental_clinic.treatment.models import Treatment


class PatientMedicalRecordViewTestCase(TestCase):
    """
    A test for context isolation (`test_patient_medical_record_context_contains_only_current_patient_rows`)
    exercises `get_context_data` directly instead of going through the test
    client/template layer, so it stays valid regardless of template
    availability/content and focuses purely on the view's data-filtering logic.
    """

    def setUp(self):
        self.user = DentistUser.objects.create_user(uin_number='9876543102', password='testpassword')
        self.patient = Patient.objects.create(
            email="patient@test.com",
            first_name="Firstname",
            last_name="Lastname",
            phone_number="1234567890",
        )
        self.other_patient = Patient.objects.create(
            email="other@test.com",
            first_name="Othername",
            last_name="Otherlast",
            phone_number="0987654321",
        )

    def test_patient_medical_record_view_unauthenticated_redirects(self):
        url = reverse('patient-medical-record', args=[self.patient.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '/authentication/login/?next=' + url, fetch_redirect_response=False
        )

    def test_patient_medical_record_view_authenticated_get_renders_template(self):
        self.client.login(uin_number='9876543102', password='testpassword')
        url = reverse('patient-medical-record', args=[self.patient.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dental_clinic/patient/patient-medical-record.html')

    def test_patient_medical_record_context_contains_only_current_patient_rows(self):
        condition = MedicalCondition.objects.create(patient=self.patient, name="Diabetes")
        MedicalCondition.objects.create(patient=self.other_patient, name="Asthma")

        allergy = Allergy.objects.create(patient=self.patient, name="Penicillin")
        Allergy.objects.create(patient=self.other_patient, name="Latex")

        history = MedicalHistoryEntry.objects.create(patient=self.patient, note="Checkup")
        MedicalHistoryEntry.objects.create(patient=self.other_patient, note="Surgery")

        note = ClinicalNote.objects.create(patient=self.patient, body="Note body")
        ClinicalNote.objects.create(patient=self.other_patient, body="Other note body")

        prescription = Prescription.objects.create(
            patient=self.patient, medication="Amoxicillin", dosage="500mg"
        )
        Prescription.objects.create(
            patient=self.other_patient, medication="Ibuprofen", dosage="200mg"
        )

        treatment = Treatment.objects.create(
            clinical_code="123", name="Filling", cost=100.0, description="Composite filling"
        )
        treatment_record = TreatmentRecord.objects.create(patient=self.patient, treatment=treatment)
        TreatmentRecord.objects.create(patient=self.other_patient, treatment=treatment)

        view = PatientMedicalRecordView()
        view.object = self.patient
        context = view.get_context_data()

        self.assertEqual(list(context['medical_conditions']), [condition])
        self.assertEqual(list(context['allergies']), [allergy])
        self.assertEqual(list(context['medical_history_entries']), [history])
        self.assertEqual(list(context['clinical_notes']), [note])
        self.assertEqual(list(context['prescriptions']), [prescription])
        self.assertEqual(list(context['treatment_records']), [treatment_record])
