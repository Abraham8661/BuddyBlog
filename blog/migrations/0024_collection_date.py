# Generated by Django 4.2.7 on 2023-12-13 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0023_remove_collection_collection_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
