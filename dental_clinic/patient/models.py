from django.db import models
from django.core.validators import MinLengthValidator
from .validators import validate_phone_number_only_nums, \
    validate_name_contain_only_letters, \
    validate_name_start_with_capital_letter
from ..treatment.models import Treatment


class Patient(models.Model):
    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=30, validators=(
        validate_name_start_with_capital_letter, validate_name_contain_only_letters
    ))

    last_name = models.CharField(max_length=30, validators=(
        validate_name_start_with_capital_letter, validate_name_contain_only_letters
    ))

    phone_number = models.CharField(
        max_length=10,
        validators=[MinLengthValidator(10), validate_phone_number_only_nums]
    )

    treatment = models.ManyToManyField(Treatment, blank=True)

    def delete(self, *args, **kwargs):
        self.treatment.clear()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
