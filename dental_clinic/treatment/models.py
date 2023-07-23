from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from .validators import validate_contain_only_digits


class Treatment(models.Model):
    clinical_code = models.CharField(
        max_length=3,
        validators=[
            MinLengthValidator(3), MaxLengthValidator(3), validate_contain_only_digits
        ])
    name = models.CharField(max_length=100)
    cost = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return f"{self.clinical_code}"
