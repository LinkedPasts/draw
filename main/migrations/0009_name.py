# Generated by Django 3.0.3 on 2020-06-02 19:50

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20200415_2206'),
    ]

    operations = [
        migrations.CreateModel(
            name='Name',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=200)),
                ('maps', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=10), size=None)),
            ],
            options={
                'db_table': 'names',
                'managed': True,
            },
        ),
    ]
