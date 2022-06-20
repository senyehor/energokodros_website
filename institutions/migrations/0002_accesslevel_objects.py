# Generated by Django 4.0.4 on 2022-06-20 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessLevel',
            fields=[
                ('access_level_id', models.AutoField(primary_key=True, serialize=False)),
                ('level_def', models.IntegerField(unique=True)),
                ('level_description', models.TextField()),
            ],
            options={
                'db_table': 'access_levels',
            },
        ),
        migrations.CreateModel(
            name='Objects',
            fields=[
                ('object_id', models.AutoField(primary_key=True, serialize=False)),
                ('object_name', models.CharField(blank=True, max_length=1000)),
                ('object_description', models.TextField(blank=True, null=True)),
                ('access_level', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='institutions.accesslevel')),
                ('institution', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='institutions.institution')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institutions.objects')),
            ],
            options={
                'db_table': 'objects',
            },
        ),
    ]