# Generated by Django 5.0.7 on 2024-07-27 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0001_initial'),
        ('pins', '0003_alter_pin_board'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='pin',
            field=models.ManyToManyField(related_name='pins', to='pins.pin'),
        ),
    ]
