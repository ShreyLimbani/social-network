# Generated by Django 3.0.7 on 2020-08-11 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_auto_20200811_2335'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='followers',
            new_name='relationships',
        ),
    ]