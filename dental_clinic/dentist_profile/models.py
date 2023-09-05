from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from .validators import validate_name_contain_only_letters, validate_name_start_with_capital_letter


UserModel = get_user_model()


class DentistUserProfile(models.Model):

    FIRST_NAME_MAX_LENGTH = 30
    FIRST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAX_LENGTH = 30
    LAST_NAME_MIN_LENGTH = 2

    email = models.EmailField(
        blank=True,
        null=True
    )

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=[
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            validate_name_contain_only_letters,
            validate_name_start_with_capital_letter
        ]
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=[
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            validate_name_contain_only_letters,
            validate_name_start_with_capital_letter
        ]
    )

    profile_picture = models.URLField(
        null=True,
        blank=True
    )

    user = models.OneToOneField(UserModel, primary_key=True, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
