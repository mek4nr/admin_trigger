# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('event', '0005_event_eventchangefield_triggerdate_triggerfield_triggerobject'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='object_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
