# Generated by Django 3.0.3 on 2020-03-01 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feature',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='map',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'managed': True},
        ),
        migrations.AlterModelTable(
            name='feature',
            table='features',
        ),
        migrations.AlterModelTable(
            name='map',
            table='maps',
        ),
        migrations.AlterModelTable(
            name='project',
            table='projects',
        ),
    ]