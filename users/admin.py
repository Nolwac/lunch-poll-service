from django.contrib import admin
from users.models import User
from employees.models import Employee


admin.site.register(User)
admin.site.register(Employee)
# Register your models here.
