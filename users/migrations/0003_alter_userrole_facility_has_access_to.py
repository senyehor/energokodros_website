# Generated by Django 4.1.1 on 2022-10-02 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0003_rename_facilities_facility'),
        ('users', '0002_rename_object_has_access_to_userrole_facility_has_access_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrole',
            name='facility_has_access_to',
            field=models.ForeignKey(db_column='facility_has_access_to_id', on_delete=django.db.models.deletion.CASCADE, related_name='users_roles', to='institutions.facility'),
        ),
    ]