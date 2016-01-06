# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('first_letter', models.CharField(max_length=1)),
                ('image_url', models.URLField(blank=True)),
                ('year', models.CharField(max_length=4)),
                ('genre', models.CharField(max_length=100, blank=True)),
                ('directors_list', models.CharField(max_length=3000, blank=True)),
                ('actors_list', models.TextField(blank=True)),
                ('dates', models.TextField(blank=True)),
                ('review', models.TextField(blank=True)),
                ('grade', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('first_letter', models.CharField(max_length=1)),
                ('user', models.ForeignKey(related_name='persons', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='actors',
            field=models.ManyToManyField(related_name='starred_in', blank=True, to='movies.Person'),
        ),
        migrations.AddField(
            model_name='movie',
            name='directors',
            field=models.ManyToManyField(related_name='directed', blank=True, to='movies.Person'),
        ),
        migrations.AddField(
            model_name='movie',
            name='user',
            field=models.ForeignKey(related_name='movies', to=settings.AUTH_USER_MODEL),
        ),
    ]
