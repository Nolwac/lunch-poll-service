from django.urls import reverse
from users.models import User
from django.conf import settings
from rest_framework.test import APITestCase
from rest_framework.views import status
from rest_framework.authtoken.models import Token
from users.tests.test_model import create_user

# uncomment to send email message
# settings.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# settings.DEBUG = True


def authenticate_client(obj):
    # this function authenticates the APITest object client
    api_token, created = Token.objects.get_or_create(user=obj.user)
    obj.client.credentials(HTTP_AUTHORIZATION="Token " + api_token.key)


class UserAPITest(APITestCase):
    """
    This class test the User API endpoints
    """

    def setUp(self):
        # one time setup that applies to all test
        create_user(self)

        authenticate_client(self)
        self.get_authenticated_user_url = "/api/v1/auth/user/"
        self.get_user_url = reverse("user_api:get_user", kwargs={"version": "v1", "pk": self.user.id})

    def test_user_count(self):
        response = self.client.get("/api/v1/users/", format="json")
        users_count = len(response.data)
        self.assertEquals(users_count, 1)

    def test_get_user_url_reverse(self):
        self.assertEquals(self.get_user_url, "/api/v1/users/1/")

    def test_get_authenticated_user(self):
        response = self.client.get(self.get_authenticated_user_url, format="json")
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_user(self):
        response = self.client.get(self.get_user_url, format="json")
        self.assertEquals(response.status_code, status.HTTP_200_OK)


class UserAuthAPITest(APITestCase):
    """
    This class test the User API endpoints
    """

    def setUp(self):
        # one time setup that applies to all test
        self.password = "123-9587hahsng"
        self.email = "livinusanayo96@gmail.com"
        self.first_name = "Livinus"
        self.last_name = "Nwafor"
        self.user_type = User.UserType.RESTAURANT
        self.restaurant_name = "Test Restaurant"
        self.description = "Responsible for testing food menu for our client company"
        self.username = "Nolwac"

        self.registration_url = "/api/v1/registration/"
        data = {
            "password1": self.password,
            "password2": self.password,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "user_type": self.user_type,
            "restaurant_name": self.restaurant_name,
            "description": self.description,
        }

        response = self.client.post(self.registration_url, data, format="json")
        self.auth_token = response.data["key"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.auth_token}")
        self.get_authenticated_user_url = "/api/v1/auth/user/"
        self.login_url = "/api/v1/auth/login/"
        self.logout_url = "/api/v1/auth/logout/"

    def clear_authorization(self):
        self.client.credentials(HTTP_AUTHORIZATION="")

    def set_authorization(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.auth_token}")

    def login(self):
        login_data = {"email": self.email, "password": self.password}
        response = self.client.post(self.login_url, login_data, format="json")
        self.auth_token = response.data["key"]
        self.set_authorization()
        return self.auth_token

    def logout(self):
        self.client.post(self.logout_url, {}, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="")

    def test_registration_success(self):
        response = self.client.get(self.get_authenticated_user_url, format="json")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        pk = response.data["pk"]
        user = User.objects.get(pk=pk)
        user_type = response.data["user_type"]

        self.assertEquals(user_type, self.user_type)
        self.assertEquals(user.profile.description, self.description)
        self.assertEquals(user.profile.restaurant_name, self.restaurant_name)

    def test_registration_resend_email(self):
        resend_email_url = "/api/v1/registration/resend-email/"
        resend_email_data = {"email": self.email}

        response = self.client.post(resend_email_url, resend_email_data, format="json")
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_password_change(self):
        new_password = "=wfknda9iedkkddd-do"
        password_data = {"new_password1": new_password, "new_password2": new_password}

        self.password = new_password
        password_change_url = "/api/v1/auth/password/change/"
        self.client.post(password_change_url, password_data, format="json")

        # logging out and logging in with new password
        self.logout()
        self.login()

        # checking if user can be retrieved as a proof of successful password change
        response = self.client.get(self.get_authenticated_user_url, format="json")
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_password_reset(self):
        password_reset_data = {"email": self.email}
        password_reset_url = "/api/v1/auth/password/reset/"
        response = self.client.post(password_reset_url, password_reset_data, format="json")
        self.assertEquals(response.data["detail"], "Password reset e-mail has been sent.")

    def test_user_update(self):
        user_update_url = self.get_authenticated_user_url
        new_username = "Prime"
        phone = "+2348107905404"
        user_update_data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "username": new_username,
            "phone": phone,
        }

        response = self.client.put(user_update_url, user_update_data, format="json")
        phone_response = response.data["phone"]
        username = response.data["username"]
        pk = response.data["pk"]
        user = User.objects.get(pk=pk)
        user_type = response.data["user_type"]

        self.assertEquals(user_type, self.user_type)
        self.assertEquals(phone, phone_response)
        self.assertEquals(username, new_username)
        self.assertEquals(user.profile.description, self.description)
        self.assertEquals(user.profile.restaurant_name, self.restaurant_name)
