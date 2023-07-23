from django.core.validators import ValidationError


def validate_uin_number_contains_only_nums(value):
    if not value.isdigit():
        raise ValidationError('UIN number must contain only numbers')