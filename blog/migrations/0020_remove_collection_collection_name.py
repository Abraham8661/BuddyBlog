# Generated by Django 4.2.7 on 2023-12-11 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_profile_author_followers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='collection_name',
        ),
    ]
