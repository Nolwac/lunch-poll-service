from rest_framework import serializers
from restaurants.models import Restaurant, Menu


class RestaurantSerializer(serializers.ModelSerializer[Restaurant]):
    class Meta:
        model = Restaurant
        fields = "__all__"
        read_only_fields = ["user"]


class MenuSerializer(serializers.ModelSerializer[Menu]):
    class Meta:
        model = Menu
        fields = "__all__"
