from django.db import models
from django.contrib.auth import models as auth_models
from django.core.validators import MinLengthValidator
from .validators import validate_uin_number_contains_only_nums
from django.contrib.auth.hashers import make_password


class DentalUserManager(auth_models.BaseUserManager):
    use_in_migrations = True

    def _create_user(self, uin_number, password, **extra_fields):
        if not uin_number:
            raise ValueError("The given uin number must be set")
        user = self.model(uin_number=uin_number, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, uin_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(uin_number, password, **extra_fields)

    def create_superuser(self, uin_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(uin_number, password, **extra_fields)


class DentistUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):

    USERNAME_FIELD = 'uin_number'
    UIN_NUMBER_MAX_LENGTH = 10
    UIN_NUMBER_MIN_LENGTH = 10

    objects = DentalUserManager()

    uin_number = models.CharField(
        max_length=UIN_NUMBER_MAX_LENGTH,
        validators=[
            MinLengthValidator(UIN_NUMBER_MIN_LENGTH),
            validate_uin_number_contains_only_nums
        ],
        unique=True,
        null=False,
        blank=False
    )

    is_staff = models.BooleanField(
        default=True
    )
