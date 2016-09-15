# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_tvshow_tvshowseason'),
    ]

    operations = [
        migrations.AddField(
            model_name='tvshowseason',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='tvshowseason',
            name='url_number',
            field=models.CharField(default='01', max_length=3),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tvshow',
            name='genre_family',
            field=models.CharField(max_length=100, choices=[('drama', 'драма'), ('comedy', 'комедия'), ('animated', 'анимационный'), ('fantastic', 'фантастический'), ('doc', 'документальный'), ('other', 'другое')]),
        ),
        migrations.AlterField(
            model_name='tvshowseason',
            name='number',
            field=models.IntegerField(),
        ),
    ]
