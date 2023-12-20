# Generated by Django 4.2.7 on 2023-12-09 17:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0017_remove_user_follower_new_follower_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_follower',
            name='new_follower',
        ),
        migrations.RemoveField(
            model_name='user_following',
            name='new_following',
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
    ]
