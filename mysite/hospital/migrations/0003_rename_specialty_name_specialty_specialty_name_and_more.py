# Generated by Django 5.1.6 on 2025-02-19 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0002_alter_feedback_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='specialty',
            old_name='Specialty_name',
            new_name='specialty_name',
        ),
        migrations.AddField(
            model_name='department',
            name='department_name_en',
            field=models.CharField(max_length=32, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='department',
            name='department_name_ru',
            field=models.CharField(max_length=32, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='specialty',
            name='specialty_name_en',
            field=models.CharField(max_length=32, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='specialty',
            name='specialty_name_ru',
            field=models.CharField(max_length=32, null=True, unique=True),
        ),
    ]
