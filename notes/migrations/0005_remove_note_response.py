# Generated by Django 5.0.7 on 2024-07-30 02:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_alter_note_options_remove_note_content_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='response',
        ),
    ]