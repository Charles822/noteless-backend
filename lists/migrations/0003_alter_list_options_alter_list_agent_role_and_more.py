# Generated by Django 5.0.7 on 2024-07-29 04:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_agent', '0003_agentrole_name'),
        ('lists', '0002_remove_list_notes_alter_list_agent_role_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='list',
            options={'ordering': ['-created_at'], 'verbose_name': 'List', 'verbose_name_plural': 'Lists'},
        ),
        migrations.AlterField(
            model_name='list',
            name='agent_role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ai_agent.agentrole'),
        ),
        migrations.AlterField(
            model_name='list',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
