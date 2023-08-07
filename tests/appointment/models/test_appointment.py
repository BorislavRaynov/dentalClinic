from django.test import TestCase
from dental_clinic.appointment.models import Appointment
from dental_clinic.patient.models import Patient
from dental_clinic.auth_app.models import DentistUser


class AppointmentModelTestCase(TestCase):
    def setUp(self):

        self.patient = Patient.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone_number="1234567890"
        )
        self.dentist = DentistUser.objects.create_user(
            uin_number="1234567890",
            password="testpassword"
        )

        self.appointment = Appointment.objects.create(
            patient=self.patient,
            dentist=self.dentist,
            date="2023-07-20",
            time="10:00:00"
        )

    def test_patient_foreign_key(self):
        self.assertEqual(self.appointment.patient, self.patient)

    def test_dentist_foreign_key(self):
        self.assertEqual(self.appointment.dentist, self.dentist)

    def test_date_field(self):
        self.assertEqual(self.appointment.date, "2023-07-20")

    def test_time_field(self):
        self.assertEqual(self.appointment.time, "10:00:00")
