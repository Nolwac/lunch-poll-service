from django.urls import reverse
from users.models import User
from django.conf import settings
from rest_framework.test import APITestCase
from rest_framework.views import status
from rest_framework.authtoken.models import Token
from users.tests.test_model import create_user
from users.tests.test_api import authenticate_client


class RestaurantAPITest(APITestCase):
    """
    This class test the Restaurant API endpoints
    """

    def setUp(self) -> None:
        # one time setup that applies to all test
        create_user(self, user_type=User.UserType.RESTAURANT)
        authenticate_client(self)
        self.get_restaurants_url = "/api/v1/restaurants/"

    def test_get_restaurant_info(self) -> None:
        response = self.client.get(self.get_restaurants_url, format="json")
        restaurants_count = len(response.data)
        self.assertEquals(restaurants_count, 1)

    def test_get_restaurants(self) -> None:
        response = self.client.get(self.get_restaurants_url, format="json")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 1)

    def test_get_restaurant_profile(self) -> None:
        response = self.client.get(f"{self.get_restaurants_url}{self.user.restaurant.pk}/", format="json")
        restaurant_name = response.data["restaurant_name"]
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(restaurant_name, self.restaurant_name)

    def test_update_restaurant(self) -> None:
        new_restaurant_name = "Test Update Restaurant"
        data = {"description": self.user.restaurant.description, "restaurant_name": "Test Update Restaurant"}
        response = self.client.put(f"{self.get_restaurants_url}{self.user.restaurant.pk}/", data, format="json")
        self.assertEquals(response.data["restaurant_name"], new_restaurant_name)
        restaurant_name = self.client.get(f"{self.get_restaurants_url}{self.user.restaurant.pk}/", format="json").data[
            "restaurant_name"
        ]
        self.assertEquals(new_restaurant_name, restaurant_name)

    def test_user_change_fails(self) -> None:
        dummy_obj = APITestCase()
        create_user(dummy_obj)  # to create new user for testing change
        data = {
            "user": dummy_obj.user.pk,
            "description": self.user.restaurant.description,
            "restaurant_name": "Test Update Restaurant",
        }
        response = self.client.put(f"{self.get_restaurants_url}{self.user.restaurant.pk}/", data, format="json")
        self.assertNotEquals(response.data["user"], dummy_obj.user.pk)

    def test_other_profile_update_fails(self) -> None:
        dummy_obj = APITestCase()
        create_user(dummy_obj, user_type=User.UserType.RESTAURANT)
        data = {"description": self.user.restaurant.description, "restaurant_name": "Test Update Restaurant"}
        response = self.client.put(f"{self.get_restaurants_url}2/", data, format="json")
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)


class MenuAPITest(APITestCase):
    """
    This class tests the Menu API endpoints
    """

    def setUp(self):
        # one time setup that applies to all test
        create_user(self, user_type=User.UserType.RESTAURANT)
        authenticate_client(self)
        self.get_menu_url = "/api/v1/restaurants/menu/"

    def test_create_menu(self) -> None:
        menu_description = "Sweet Food to eat, you will love it"
        menu_restaurant = self.user.restaurant.pk
        data = {
            "description": menu_description,
        }
        response = self.client.post(self.get_menu_url, data, format="json")
        self.assertEquals(menu_restaurant, response.data["restaurant"])
        self.assertEquals(menu_description, response.data["description"])

    def test_employee_forbidden(self) -> None:
        # test that employee is forbidden from creating menu
        menu_description = "Sweet Food to eat, you will love it"
        create_user(self)  # creates an employee user and overwrites the previous
        authenticate_client(self)
        data = {
            "description": menu_description,
            "restaurant": 1,
        }
        response = self.client.post(self.get_menu_url, data, format="json")
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
