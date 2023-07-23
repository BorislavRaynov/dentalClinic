from django.core.validators import ValidationError


def validate_contain_only_digits(value):
    if not value.isdigit():
        raise ValidationError('Clinical code must contain only numbers')
