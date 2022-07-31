from rest_framework import mixins
from rest_framework import generics
from users.api.serializers import UserSerializer
from users.models import User


class UserAPIView(mixins.RetrieveModelMixin, mixins.ListModelMixin, generics.GenericAPIView):  # type: ignore
    """
    User Retrieval API
    """

    serializer_class = UserSerializer

    def get(self, request, pk=None, **kwargs):
        if pk is None:
            return self.list(request, **kwargs)
        return self.retrieve(request, pk=pk, **kwargs)

    def get_queryset(self):
        return User.objects.all()  # type: ignore
