# Generated by Django 5.0.6 on 2024-06-19 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pins', '0010_remove_pin_file_pin_image_pin_pin_image_url_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pin',
            old_name='pin_image_url',
            new_name='image_url',
        ),
        migrations.RenameField(
            model_name='pin',
            old_name='pin_video_url',
            new_name='video_url',
        ),
    ]
