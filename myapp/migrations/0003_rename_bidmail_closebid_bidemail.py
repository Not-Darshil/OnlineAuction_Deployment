# Generated by Django 5.0 on 2024-01-14 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_bidding_bidemail_closebid_bidmail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='closebid',
            old_name='bidmail',
            new_name='bidemail',
        ),
    ]