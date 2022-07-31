from django.urls import path
from users.api.views import UserAPIView


urlpatterns = [
    path("", UserAPIView.as_view(), name="list_user"),
    path("<int:pk>/", UserAPIView.as_view(), name="get_user"),
]
