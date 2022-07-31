from django.test import TestCase
from users.models import User


class UserTestCase(TestCase):
    def setUp(self):
        self.password = "123-9587hahsng"
        self.user = User.objects.create_user(
            email="livinusanayo96@gmail.com",
            username="Nolwac",
            password=self.password,
            first_name="Livinus",
            last_name="Nwafor",
        )

    def test_that_user_is_correctly_created(self):
        self.assertEqual(self.user.username, "Nolwac")
        self.assertEqual(self.user.first_name, "Livinus")
        self.assertEqual(self.user.email, "livinusanayo96@gmail.com")
        self.assertNotEqual(self.user.password, self.password)

    def test_email_is_compulsory(self):
        with self.assertRaises(TypeError):
            User.objects.create_user(
                username="Nolwac", first_name="Livinus", last_name="Nwafor", password="some709u0-gibrerish"
            )
