# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_auto_20160915_0108'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='date_created',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='date_edited',
            field=models.DateField(null=True, auto_now=True),
        ),
    ]
