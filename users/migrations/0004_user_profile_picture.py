# Generated by Django 4.2.7 on 2023-12-08 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_first_name_alter_user_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(default='blog/images/blank-picture.png', upload_to='images'),
        ),
    ]
