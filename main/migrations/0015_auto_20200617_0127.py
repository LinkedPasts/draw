# Generated by Django 3.0.3 on 2020-06-17 01:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20200611_2204'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feature',
            old_name='name',
            new_name='title',
        ),
        migrations.AddField(
            model_name='feature',
            name='src_name',
            field=models.ForeignKey(db_column='src_name', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='src_name', to='main.Name'),
        ),
    ]
