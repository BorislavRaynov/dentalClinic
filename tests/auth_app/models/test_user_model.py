from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


UserModel = get_user_model()


class DentistUserModelTestCase(TestCase):

    def test_create_user_with_valid_data_create_the_user(self):
        obj = UserModel.objects.create(uin_number="1234567890", password="testpassword")
        self.assertEqual(obj.uin_number, "1234567890")
        self.assertEqual(obj.password, "testpassword")


    def test_uin_number_validator_including_letter_raises(self):
        with self.assertRaises(ValidationError):
            obj = UserModel.objects.create(uin_number="98765a3210", password="testpassword")
            obj.full_clean()
