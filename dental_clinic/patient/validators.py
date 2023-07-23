from django.core.exceptions import ValidationError


def validate_phone_number_only_nums(value):
    if not value.isdigit():
        raise ValidationError('Phone number must contain only numbers.')
