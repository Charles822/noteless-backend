# Generated by Django 5.0.7 on 2024-07-27 01:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ai_agent', '0001_initial'),
        ('contents', '0003_alter_transcript_transcript_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('response', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ai_agent.response')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contents.video')),
            ],
        ),
    ]