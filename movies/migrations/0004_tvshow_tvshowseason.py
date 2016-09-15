# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0003_auto_20160124_1353'),
    ]

    operations = [
        migrations.CreateModel(
            name='TVShow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('image_url', models.URLField(blank=True)),
                ('genre', models.CharField(max_length=100, blank=True)),
                ('genre_family', models.CharField(max_length=100, blank=True)),
                ('creators_list', models.CharField(max_length=3000, blank=True)),
                ('creators', models.ManyToManyField(related_name='created', blank=True, to='movies.Person')),
                ('user', models.ForeignKey(related_name='tvshows', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TVShowSeason',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('number', models.CharField(max_length=255)),
                ('image_url', models.URLField(blank=True)),
                ('year', models.CharField(max_length=10)),
                ('actors_list', models.TextField(blank=True)),
                ('dates', models.TextField(blank=True)),
                ('first_date', models.DateField()),
                ('review', models.TextField(blank=True)),
                ('grade', models.IntegerField(default=0)),
                ('actors', models.ManyToManyField(related_name='tvshowseason_starred_in', blank=True, to='movies.Person')),
                ('tvshow', models.ForeignKey(related_name='seasons', to='movies.TVShow')),
                ('user', models.ForeignKey(related_name='tvshowseasons', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
