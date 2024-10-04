# Generated by Django 5.0.7 on 2024-07-30 02:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_agent', '0011_alter_agentresponse_agent_role'),
        ('notes', '0005_remove_note_response'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='response',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ai_agent.agentresponse'),
        ),
    ]