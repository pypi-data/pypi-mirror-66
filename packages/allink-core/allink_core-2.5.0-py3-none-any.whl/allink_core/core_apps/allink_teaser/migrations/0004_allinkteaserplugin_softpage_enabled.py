# Generated by Django 2.2.7 on 2020-01-23 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_teaser', '0003_auto_20190716_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkteaserplugin',
            name='softpage_enabled',
            field=models.BooleanField(default=True, help_text='If checked, the detail view of an entry will be displayed in a "softpage". Otherwise the page will be reloaded.', verbose_name='Show detailed information in Softpage'),
        ),
    ]
