# Generated by Django 4.0.4 on 2022-05-12 14:05

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0002_delete_eventstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='company_name',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='client',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 5, 12, 14, 4, 16, 910765, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='client',
            name='email',
            field=models.EmailField(default='email', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='first_name',
            field=models.CharField(default='first name', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='last_name',
            field=models.CharField(default='last name', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='mobile',
            field=models.CharField(default='0025', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='phone',
            field=models.CharField(default='0021', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='sales_contact',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
