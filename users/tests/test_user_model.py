from django.test import TestCase
from users.models import User
from django.core.exceptions import ValidationError


def creat_user(self: TestCase) -> None:
    self.password = "123-9587hahsng"
    self.email = "livinusanayo96@gmail.com"
    self.first_name = "Livinus"
    self.last_name = "Nwafor"
    self.user_type = User.UserType.EMPLOYEE
    self.job_title = "Test Engineer"
    self.description = "Responsible for testing software"
    self.username = "Nolwac"
    self.user = User.objects.create_user(
        email=self.email,
        username=self.username,
        password=self.password,
        first_name=self.first_name,
        last_name=self.last_name,
        user_type=User.UserType.EMPLOYEE,
        job_title=self.job_title,
        description=self.description,
    )


class UserTestCase(TestCase):
    def setUp(self):
        creat_user(self)

    def test_that_user_is_correctly_created(self) -> None:
        self.assertEqual(self.user.username, self.username)
        self.assertEqual(self.user.first_name, self.first_name)
        self.assertEqual(self.user.email, self.email)
        self.assertEqual(self.user.user_type, self.user_type)
        self.assertEqual(self.user.profile.job_title, self.job_title)
        self.assertEqual(self.user.profile.description, self.description)
        self.assertNotEqual(self.user.password, self.password)

    def test_email_is_compulsory(self):
        with self.assertRaises(TypeError):
            User.objects.create_user(
                username="Nolwac2",
                first_name="Livinus",
                last_name="Nwafor",
                password="some709u0-gibrerish",
                job_title=self.job_title,
                description=self.description,
                user_type=self.user_type,
            )

    def test_that_unwanted_field_raises_error(self) -> None:
        with self.assertRaises(TypeError):
            User.objects.create_user(
                username="Nolwac3",
                email="example@example.com",
                first_name="Livinus",
                last_name="Nwafor",
                password="some709u0-gibrerish",
                job_title=self.job_title,
                description=self.description,
                user_type=self.user_type,
                restaurant_name="Test Restaurant",
            )

    def test_that_user_type_change_fails(self) -> None:
        with self.assertRaises(ValidationError):
            self.user.user_type = User.UserType.RESTAURANT
            self.user.save()
