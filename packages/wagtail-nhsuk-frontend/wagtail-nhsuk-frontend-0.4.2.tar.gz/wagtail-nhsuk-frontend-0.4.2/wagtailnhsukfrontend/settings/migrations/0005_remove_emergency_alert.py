# Generated by Django 2.1.9 on 2019-11-13 11:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailnhsukfrontendsettings', '0004_footersettings_fixed_coloumn_footer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emergencyalert',
            name='site',
        ),
        migrations.DeleteModel(
            name='EmergencyAlert',
        ),
    ]
