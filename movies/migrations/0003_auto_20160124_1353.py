# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations


def set_first_date_for_movies(apps, schema_editor):
    Movie = apps.get_model('movies', 'Movie')
    for movie in Movie.objects.all():
        date = movie.dates.split(', ')[0]
        year, month, day = [int(elem) for elem in date.split('-')]
        movie.first_date = datetime.date(year, month, day)
        movie.save()


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20160124_1352'),
    ]

    operations = [
        migrations.RunPython(set_first_date_for_movies)
    ]
