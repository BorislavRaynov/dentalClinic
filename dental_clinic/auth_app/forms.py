from django import forms
from django.contrib.auth import forms as auth_forms
from dental_clinic.dentist_profile.models import DentistUserProfile
from django.core.validators import MinLengthValidator
from dental_clinic.dentist_profile.validators import \
    validate_name_contain_only_letters, \
    validate_name_start_with_capital_letter
from django.contrib.auth import get_user_model


UserModel = get_user_model()

class RegisterUserForm(auth_forms.UserCreationForm):

    first_name = forms.CharField(
        max_length=DentistUserProfile.FIRST_NAME_MAX_LENGTH,
        validators=[
            MinLengthValidator(DentistUserProfile.FIRST_NAME_MIN_LENGTH),
            validate_name_contain_only_letters,
            validate_name_start_with_capital_letter
        ],
        required=True
    )

    last_name = forms.CharField(
        max_length=DentistUserProfile.LAST_NAME_MAX_LENGTH,
        validators=[
            MinLengthValidator(DentistUserProfile.LAST_NAME_MIN_LENGTH),
            validate_name_contain_only_letters,
            validate_name_start_with_capital_letter
        ],
        required=True
    )

    profile_picture = forms.URLField(required=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password2'].label = 'Repeat password'

        for field in self.fields.values():
            field.help_text = None

    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = ['uin_number']

    def save(self, commit=True):
        user = super().save(commit)

        profile = DentistUserProfile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            profile_picture=self.cleaned_data['profile_picture'],
            user=user
        )

        if commit:
            profile.save()

        return user
