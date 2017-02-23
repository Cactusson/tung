# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_auto_20160915_0108'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='date_created',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='date_edited',
            field=models.DateField(null=True, auto_now=True),
        ),
        migrations.AddField(
            model_name='tvshow',
            name='date_created',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='tvshow',
            name='date_edited',
            field=models.DateField(null=True, auto_now=True),
        ),
        migrations.AddField(
            model_name='tvshowseason',
            name='date_created',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='tvshowseason',
            name='date_edited',
            field=models.DateField(null=True, auto_now=True),
        ),
    ]
