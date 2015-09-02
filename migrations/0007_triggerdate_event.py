# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0006_auto_20150418_2017'),
    ]

    operations = [
        migrations.AddField(
            model_name='triggerdate',
            name='event',
            field=models.ForeignKey(to='event.Event', default=1),
            preserve_default=False,
        ),
    ]
