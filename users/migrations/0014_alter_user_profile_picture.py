# Generated by Django 4.2.7 on 2023-12-09 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_user_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
    ]
