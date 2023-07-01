# Generated by Django 3.2.19 on 2023-06-29 05:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_add_publishers'),
    ]

    operations = [
        migrations.AddField(
            model_name='linktype',
            name='weight',
            field=models.PositiveIntegerField(default=10, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
    ]