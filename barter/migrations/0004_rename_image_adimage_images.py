# Generated by Django 5.2.1 on 2025-05-24 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barter', '0003_remove_ad_image_adimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adimage',
            old_name='image',
            new_name='images',
        ),
    ]
