from django.db import models
from django.core.validators import MinLengthValidator
from .validators import validate_contain_only_digits


class Treatment(models.Model):

    MIN_CLINICAL_CODE_LENGTH = 3
    MAX_CLINICAL_CODE_LENGTH = 3

    clinical_code = models.CharField(
        max_length=MAX_CLINICAL_CODE_LENGTH,
        validators=[
            MinLengthValidator(MIN_CLINICAL_CODE_LENGTH), validate_contain_only_digits
        ])
    name = models.CharField(max_length=100)
    cost = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return f"{self.clinical_code}"
