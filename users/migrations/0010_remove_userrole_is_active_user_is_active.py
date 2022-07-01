# Generated by Django 4.0.5 on 2022-07-01 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_userrole_is_active_delete_userregistrationdata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userrole',
            name='is_active',
        ),
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='чи підтвердив користувач пошту'),
        ),
    ]
