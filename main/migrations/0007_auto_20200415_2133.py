# Generated by Django 3.0.3 on 2020-04-15 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20200415_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='tiles',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='map',
            name='year',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='map',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
