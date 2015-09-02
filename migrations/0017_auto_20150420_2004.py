# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('event', '0016_foreignevent_classname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foreignevent',
            name='event_ptr',
        ),
        migrations.DeleteModel(
            name='ForeignEvent',
        ),
        migrations.AddField(
            model_name='eventchangefield',
            name='content_type',
            field=models.ForeignKey(default=1, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventchangefield',
            name='object_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
