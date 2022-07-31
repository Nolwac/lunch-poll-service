from rest_framework import serializers
from users.models import User
from dj_rest_auth.serializers import PasswordResetSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.forms import PasswordResetForm


class RegistrationSerializer(RegisterSerializer):
    phone = PhoneNumberField(required=False)
    first_name = serializers.CharField(required=False, max_length=20)
    last_name = serializers.CharField(required=False, max_length=50)

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict["phone"] = self.validated_data.get("phone", None)
        data_dict["first_name"] = self.validated_data.get("first_name", None)
        data_dict["last_name"] = self.validated_data.get("last_name", None)
        return data_dict


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "phone", "pk"]


class UserPasswordResetSerializer(PasswordResetSerializer):
    @property
    def password_reset_form_class(self):
        return PasswordResetForm
