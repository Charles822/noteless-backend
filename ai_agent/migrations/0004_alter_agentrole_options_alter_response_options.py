# Generated by Django 5.0.7 on 2024-07-29 04:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ai_agent', '0003_agentrole_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agentrole',
            options={'ordering': ['name'], 'verbose_name': 'Agent Role', 'verbose_name_plural': 'Agent Roles'},
        ),
        migrations.AlterModelOptions(
            name='response',
            options={'ordering': ['-created_at'], 'verbose_name': 'Response', 'verbose_name_plural': 'Responses'},
        ),
    ]