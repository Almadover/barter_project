# Generated by Django 5.2.1 on 2025-05-24 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barter', '0004_rename_image_adimage_images'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adimage',
            old_name='images',
            new_name='image',
        ),
    ]
