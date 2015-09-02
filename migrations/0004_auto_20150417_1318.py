# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_tanukitriggerdate_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tanukieventchange',
            name='event',
        ),
        migrations.DeleteModel(
            name='TanukiEventChange',
        ),
        migrations.RemoveField(
            model_name='tanukieventhandler',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='tanukitriggerdate',
            name='event',
        ),
        migrations.DeleteModel(
            name='TanukiEventHandler',
        ),
        migrations.DeleteModel(
            name='TanukiTriggerDate',
        ),
    ]
