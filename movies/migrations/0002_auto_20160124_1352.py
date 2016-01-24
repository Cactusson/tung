# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='first_date',
            field=models.DateField(default=datetime.datetime(2016, 1, 24, 10, 52, 22, 52788, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='movie',
            name='first_letter',
            field=models.CharField(max_length=1, blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='first_letter',
            field=models.CharField(max_length=1, blank=True),
        ),
    ]
