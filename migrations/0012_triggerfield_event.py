# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0011_auto_20150418_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='triggerfield',
            name='event',
            field=models.ForeignKey(to='event.Event', default=1),
            preserve_default=False,
        ),
    ]
