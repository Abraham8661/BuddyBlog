# Generated by Django 4.2.7 on 2023-12-11 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_collection_collection_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='collection_name',
        ),
    ]
