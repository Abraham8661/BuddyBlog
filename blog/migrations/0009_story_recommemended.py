# Generated by Django 4.2.7 on 2023-12-06 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_alter_category_short_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='recommemended',
            field=models.BooleanField(default=False, help_text='No=Not Recommemended, Yes=Recommemended', null=True),
        ),
    ]
