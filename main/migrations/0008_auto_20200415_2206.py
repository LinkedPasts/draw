# Generated by Django 3.0.3 on 2020-04-15 22:06

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20200415_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='bounds',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=8, max_digits=11), null=True, size=None),
        ),
        migrations.AlterField(
            model_name='map',
            name='maxzoom',
            field=models.CharField(max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='map',
            name='minzoom',
            field=models.CharField(max_length=2, null=True),
        ),
    ]