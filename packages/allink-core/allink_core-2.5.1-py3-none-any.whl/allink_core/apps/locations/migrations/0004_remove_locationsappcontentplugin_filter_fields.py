# Generated by Django 2.1.10 on 2019-10-02 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_locations_commercial_register_entry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locationsappcontentplugin',
            name='filter_fields',
        ),
    ]
