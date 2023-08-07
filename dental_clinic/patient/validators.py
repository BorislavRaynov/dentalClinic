from django.core.exceptions import ValidationError


def validate_phone_number_only_nums(value):
    if not value.isdigit():
        raise ValidationError('Phone number must contain only numbers.')


def validate_name_contain_only_letters(value):
    if not value.isalpha():
        raise ValidationError('Name can contain only letters.')


def validate_name_start_with_capital_letter(value):
    if not value[0].isupper():
        raise ValidationError('Name must start with capital letter.')
