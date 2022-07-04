# Generated by Django 4.0.5 on 2022-06-29 09:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_rename_registration_date_userregistrationdata_applied_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userroleapplication',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registration_requests', to=settings.AUTH_USER_MODEL),
        ),
    ]