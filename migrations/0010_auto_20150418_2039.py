# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0009_auto_20150418_2034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='event',
            name='object_id',
        ),
    ]
