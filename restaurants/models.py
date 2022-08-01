from django.db import models


class Restaurant(models.Model):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE, null=False)
    restaurant_name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
