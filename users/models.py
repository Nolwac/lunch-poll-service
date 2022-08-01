from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.base_user import BaseUserManager
from typing import TypeVar, Union, Optional
from employees.models import Employee
from restaurants.models import Restaurant
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager["User"]):
    use_in_migrations = True

    def _create_user(self, email: str, password: str, **extra_fields):
        if not email:
            raise ValueError("an email field is required")
        email = self.normalize_email(email)
        username = extra_fields.pop("username", None)
        first_name = extra_fields.pop("first_name", None)
        last_name = extra_fields.pop("last_name", None)
        phone = extra_fields.pop("phone", None)
        user_type = extra_fields.pop("user_type", None)
        is_staff = extra_fields.pop("is_staff", None)
        is_superuser = extra_fields.pop("is_superuser", None)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            user_type=user_type,
        )
        user.set_password(password)

        profile_object: Union[Employee, Restaurant]
        if user.user_type == User.UserType.EMPLOYEE:
            employee = Employee(**extra_fields)
            profile_object = employee
        else:
            restaurant = Restaurant(**extra_fields)
            profile_object = restaurant

        profile_object.full_clean(exclude=["user"], validate_unique=True)
        user.save(using=self._db)
        profile_object.user = user
        profile_object.save(using=self._db)
        return user

    def create_user(self, email: str, password: str = None, **extra_fields):
        extra_fields.setdefault("user_type", User.UserType.EMPLOYEE)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields):
        extra_fields.setdefault("user_type", User.UserType.EMPLOYEE)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("job_title", "System Administrator")
        extra_fields.setdefault("description", "A system administrator managing")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    class UserType(models.TextChoices):
        EMPLOYEE = "EMPLOYEE", _("Employee")
        RESTAURANT = "RESTAURANT", _("Restaurant")

    first_name = models.CharField(_("first name"), max_length=50, null=True, blank=False)
    last_name = models.CharField(_("last name"), max_length=50, null=True, blank=False)
    email = models.EmailField(_("email address"), max_length=50, unique=True)
    phone = PhoneNumberField(_("phone number"), null=True, blank=False, unique=True)
    user_type = models.CharField(max_length=10, null=False, blank=False, choices=UserType.choices)
    REQUIRED_FIELDS = ["email", "user_type"]

    objects = UserManager()  # type: ignore

    @property
    def profile(self) -> Union[Employee, Restaurant]:
        if self.user_type == self.UserType.EMPLOYEE:
            return self.employee
        else:
            return self.restaurant

    def save(self, *args, **kwargs) -> None:
        # validate that the user type hasn't changed
        if not self._state.adding:
            try:
                # test accessing profile property still works as should
                self.profile
            except Exception:
                raise ValidationError({"user_type": _("user_type can not be modified")})
        super().save(*args, **kwargs)
