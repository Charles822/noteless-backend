# Generated by Django 5.1.1 on 2024-11-18 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_profile_credit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='credit',
            field=models.IntegerField(default=20),
        ),
    ]
