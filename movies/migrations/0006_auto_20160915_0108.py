# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_auto_20160914_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='image_url',
            field=models.URLField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='tvshow',
            name='image_url',
            field=models.URLField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='tvshowseason',
            name='image_url',
            field=models.URLField(blank=True, max_length=1000),
        ),
    ]
