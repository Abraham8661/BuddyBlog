# Generated by Django 4.2.7 on 2023-12-09 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_profile_chosen_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]
