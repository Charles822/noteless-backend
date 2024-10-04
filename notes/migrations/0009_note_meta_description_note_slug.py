# Generated by Django 5.1.1 on 2024-09-29 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0008_note_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='meta_description',
            field=models.TextField(blank=True, max_length=160),
        ),
        migrations.AddField(
            model_name='note',
            name='slug',
            field=models.SlugField(blank=True, max_length=60),
        ),
    ]