# Generated by Django 5.1.6 on 2025-02-20 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0010_alter_doctor_shift_end_alter_doctor_shift_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='service_price',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
