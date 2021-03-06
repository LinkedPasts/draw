# Generated by Django 3.0.3 on 2020-03-09 23:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0003_auto_20200307_0339'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='map',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='maps', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='uri',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='ProjectUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('creator', 'Creator'), ('owner', 'Owner'), ('member', 'Team Member')], max_length=20)),
                ('project', models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='main.Project')),
                ('user', models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'project_user',
                'managed': True,
            },
        ),
    ]
