# Generated by Django 4.2.7 on 2023-12-09 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_profile_bio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='profile_picture',
        ),
    ]
