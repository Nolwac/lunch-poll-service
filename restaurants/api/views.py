from rest_framework import mixins
from rest_framework import generics
from restaurants.api.serializers import MenuSerializer, RestaurantSerializer
from restaurants.models import Menu, Restaurant
from typing import Union
from restaurants.api.permissions import IsOwnerOrReadOnly, IsProfileOrReadOnly


class MenuView(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    generics.GenericAPIView,  # type: ignore
):
    """
    Menu API
    """

    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = MenuSerializer

    def get(self, request, pk: Union[int, None] = None, **kwargs):
        if pk is not None:
            return self.retrieve(request, pk, **kwargs)
        return self.list(request, pk, **kwargs)

    def post(self, request, **kwargs):
        return self.create(request, **kwargs)

    def delete(self, request, pk: int, **kwargs):
        return self.destroy(request, pk=None, **kwargs)

    def put(self, request, pk: int, **kwargs):
        return self.update(request, pk=None, **kwargs)

    def get_queryset(self):
        return Menu.objects.all()


class RestaurantView(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    generics.GenericAPIView,  # type: ignore
):
    """
    Restaurant API
    """

    permission_classes = [IsProfileOrReadOnly]
    serializer_class = RestaurantSerializer

    def get(self, request, pk: Union[int, None] = None, **kwargs):
        if pk is not None:
            return self.retrieve(request, pk, **kwargs)
        return self.list(request, pk, **kwargs)

    def put(self, request, pk: int, **kwargs):
        return self.update(request, pk=None, **kwargs)

    def get_queryset(self):
        return Restaurant.objects.all()
