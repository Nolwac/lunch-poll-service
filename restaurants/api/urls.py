from django.urls import path
from restaurants.api.views import MenuView, RestaurantView


urlpatterns = [
    path("", RestaurantView.as_view(), name="list_restaurant"),
    path("<int:pk>/", RestaurantView.as_view(), name="get_restaurant"),
    path("<int:pk>/update", RestaurantView.as_view(), name="update_restaurant"),
    path("menu/", MenuView.as_view(), name="list_create_menu"),
    path("menu/<int:pk>/", MenuView.as_view(), name="get_menu"),
    path("menu/<int:pk>/delete", MenuView.as_view(), name="delete_menu"),
    path("menu/<int:pk>/update", MenuView.as_view(), name="update_menu"),
]
