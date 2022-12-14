# Generated by Django 4.0.6 on 2022-07-31 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_user_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="user_type",
            field=models.CharField(
                choices=[("EMPLOYEE", "Employee"), ("RESTAURANT", "Restaurant")], default="EMPLOYEE", max_length=10
            ),
            preserve_default=False,
        ),
    ]
