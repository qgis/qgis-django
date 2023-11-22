# Generated by Django 2.2.25 on 2023-06-17 03:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('plugins', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PluginVersionFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.TextField(help_text='A feedback task. Please write your review as a task for this plugin.', max_length=1000, verbose_name='Task')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('completed_on', models.DateTimeField(blank=True, null=True, verbose_name='Completed on')),
                ('is_completed', models.BooleanField(db_index=True, default=False, verbose_name='Completed')),
                ('reviewer', models.ForeignKey(help_text='The user who reviewed this plugin.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Reviewed by')),
                ('version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to='plugins.PluginVersion')),
            ],
            options={
                'ordering': ['created_on'],
            },
        ),
    ]
