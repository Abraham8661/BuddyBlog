# Generated by Django 4.2.7 on 2023-12-09 16:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0015_remove_user_following_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_following',
            name='users_to_follow',
        ),
        migrations.AddField(
            model_name='user_follower',
            name='new_follower',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='new_follower', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user_following',
            name='new_following',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='new_following', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user_following',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='user_follower',
            name='user',
        ),
        migrations.AddField(
            model_name='user_follower',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
