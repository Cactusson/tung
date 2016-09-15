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
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('first_letter', models.CharField(max_length=1, blank=True)),
                ('user', models.ForeignKey(related_name='authors', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('image_url', models.URLField(blank=True)),
                ('year', models.CharField(max_length=4)),
                ('genre', models.CharField(max_length=100, blank=True)),
                ('authors_list', models.CharField(max_length=3000, blank=True)),
                ('dates', models.TextField(blank=True)),
                ('first_date', models.DateField()),
                ('review', models.TextField(blank=True)),
                ('grade', models.IntegerField(default=0)),
                ('authors', models.ManyToManyField(related_name='written', to='books.Author', blank=True)),
                ('user', models.ForeignKey(related_name='books', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
