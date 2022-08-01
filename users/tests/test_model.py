from typing import Union
from django.test import TestCase
from users.models import User
from django.core.exceptions import ValidationError
import random
import string


def create_user(
    self: TestCase, user_type: Union[User.UserType.EMPLOYEE, User.UserType.RESTAURANT] = User.UserType.EMPLOYEE
) -> None:
    random_string1 = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
    random_string2 = "".join(random.choices(string.ascii_uppercase + string.digits, k=9))
    self.password = "123-9587hahsng"
    self.email = f"{random_string1}@gmail.com"
    self.first_name = "Livinus"
    self.last_name = "Nwafor"
    self.username = (
        f"{random_string1}{random_string2}"  # probability of failure, approximately zero, 1 in a billion billion
    )
    self.user_type = user_type
    data = {
        "email": self.email,
        "password": self.password,
        "first_name": self.first_name,
        "last_name": self.last_name,
        "username": self.username,
        "user_type": self.user_type,
    }
    if user_type == User.UserType.EMPLOYEE:
        self.job_title = "Test Engineer"
        self.description = "Responsible for testing software"
        data.setdefault("job_title", self.job_title)
    else:
        self.restaurant_name = "Test Restaurant"
        self.description = "Responsible for testing Food Menu for Clients"
        data.setdefault("restaurant_name", self.restaurant_name)
    data.setdefault("description", self.description)
    self.user = User.objects.create_user(**data)


class UserTestCase(TestCase):
    def setUp(self):
        create_user(self)

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
