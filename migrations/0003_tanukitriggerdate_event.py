# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_auto_20150405_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='tanukitriggerdate',
            name='event',
            field=models.ForeignKey(default=1, to='event.TanukiEventHandler'),
            preserve_default=False,
        ),
    ]
