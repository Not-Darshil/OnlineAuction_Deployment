# Generated by Django 5.0 on 2024-01-15 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_closebid_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='closebid',
            name='description',
            field=models.CharField(default='', max_length=512, null=True),
        ),
    ]
