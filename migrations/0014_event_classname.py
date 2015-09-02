# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0013_auto_20150419_0234'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='classname',
            field=models.CharField(null=True, blank=True, max_length=100),
            preserve_default=True,
        ),
    ]
