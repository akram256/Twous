# Generated by Django 2.2.2 on 2020-11-12 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Jobs', '0002_auto_20201112_1247'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bids',
            name='provider',
        ),
    ]