# Generated by Django 2.2.2 on 2020-11-12 12:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Jobs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='provider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
