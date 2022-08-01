from django.test import TestCase
from users.models import User
from django.core.exceptions import ValidationError
from users.tests.test_model import create_user
from restaurants.models import Menu


class MenuTestCase(TestCase):
    def setUp(self):
        create_user(self, user_type=User.UserType.RESTAURANT)

    def test_that_restaurant_can_create_menu(self) -> None:
        description = "Test Menu, sweet food"
        menu = Menu.objects.create(restaurant=self.user.restaurant, description=description)
        self.assertEqual(Menu.objects.count(), 1)
        self.assertEqual(menu.restaurant, self.user.restaurant)
        self.assertEqual(menu.description, description)
