# Generated by Django 4.0.4 on 2022-06-20 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0004_alter_object_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='object',
            name='access_level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='+', to='institutions.accesslevel'),
        ),
    ]