# Generated by Django 3.0.3 on 2020-03-04 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adventure', '0002_auto_20200304_1757'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='id_room',
        ),
        migrations.RemoveField(
            model_name='room',
            name='move_x',
        ),
        migrations.RemoveField(
            model_name='room',
            name='move_y',
        ),
    ]