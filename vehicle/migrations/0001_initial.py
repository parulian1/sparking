# Generated by Django 4.0.9 on 2023-02-06 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_plate', models.CharField(max_length=12)),
                ('type', models.CharField(choices=[('scooters', 'Skutik/bebek'), ('medium', 'Dibawah 500cc'), ('big', 'Diatas 500cc'), ('electric', 'elektrik')], default='scooters', max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date/time this object was created.', verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date/time this object was last updated.', verbose_name='modified')),
            ],
            options={
                'db_table': 'vehicle_vehicle',
            },
        ),
    ]