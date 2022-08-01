from django.db import models

from restaurants.models import Menu
from django.core.validators import MaxValueValidator, MinValueValidator


class Employee(models.Model):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE, null=False)
    job_title = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=False, blank=False)


class MenuVote(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=False)
    date_voted = models.DateField(auto_now=False, auto_now_add=True)
    points = models.IntegerField(default=1, validators=[MaxValueValidator(3), MinValueValidator(1)])
