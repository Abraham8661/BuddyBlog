# Generated by Django 4.2.7 on 2023-12-16 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0033_profiles'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_following',
            name='new_following',
        ),
        migrations.RemoveField(
            model_name='user_following',
            name='user',
        ),
        migrations.DeleteModel(
            name='User_Follower',
        ),
        migrations.DeleteModel(
            name='User_Following',
        ),
    ]
