# Generated by Django 4.0.4 on 2022-05-12 15:38

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0005_alter_contract_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='id',
        ),
        migrations.AddField(
            model_name='event',
            name='attendees',
            field=models.IntegerField(default=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='contract',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='clients.contract'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 5, 12, 15, 37, 2, 11362, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='event',
            name='event_date',
            field=models.DateTimeField(default='2022-05-21 14:00:00'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='event_status',
            field=models.CharField(choices=[('IN PROGRESS', 'In progress'), ('FINISHED', 'Finished')], default='in progress', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='notes',
            field=models.TextField(default='rien'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='support_contact',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
