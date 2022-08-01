from typing_extensions import reveal_type
from rest_framework import serializers
from users.models import User
from dj_rest_auth.serializers import PasswordResetSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.forms import PasswordResetForm
from typing import Any, Dict, Union
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.core.exceptions import ValidationError as DjangoValidationError


class RegistrationSerializer(RegisterSerializer):
    phone = PhoneNumberField(required=False)
    first_name = serializers.CharField(required=False, max_length=20)
    last_name = serializers.CharField(required=False, max_length=50)
    user_type = serializers.ChoiceField(User.UserType.choices, required=True)
    job_title = serializers.CharField(required=False, max_length=50)
    restaurant_name = serializers.CharField(required=False, max_length=50)
    description = serializers.CharField(required=True, max_length=5000)

    def get_cleaned_data(self) -> Dict[str, Union[Any, str]]:
        data_dict = super().get_cleaned_data()
        data_dict["phone"] = self.validated_data.get("phone", None)
        data_dict["first_name"] = self.validated_data.get("first_name", None)
        data_dict["last_name"] = self.validated_data.get("last_name", None)
        data_dict["user_type"] = self.validated_data.get("user_type", None)
        if data_dict["user_type"] == User.UserType.EMPLOYEE:
            data_dict["job_title"] = self.validated_data.get("job_title", None)
        else:
            data_dict["restaurant_name"] = self.validated_data.get("restaurant_name", None)
        data_dict["description"] = self.validated_data.get("description", None)
        return data_dict

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data["password1"], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(detail=serializers.as_serializer_error(exc))

        password = self.cleaned_data.pop("password1")
        user = User.objects.create_user(password=password, **self.cleaned_data)  # type: ignore
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "user_type", "phone", "pk"]
        read_only_fields = ["user_type"]


class UserPasswordResetSerializer(PasswordResetSerializer):
    @property
    def password_reset_form_class(self):
        return PasswordResetForm
