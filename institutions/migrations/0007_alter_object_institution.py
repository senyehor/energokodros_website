# Generated by Django 4.0.4 on 2022-06-20 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0006_alter_object_institution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='object',
            name='institution',
            field=models.ForeignKey(default=53660658, on_delete=django.db.models.deletion.CASCADE, related_name='related_objects', to='institutions.institution'),
            preserve_default=False,
        ),
    ]