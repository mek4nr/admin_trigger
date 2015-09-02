# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0015_auto_20150420_1937'),
    ]

    operations = [
        migrations.AddField(
            model_name='foreignevent',
            name='classname',
            field=models.CharField(null=True, max_length=100, blank=True),
            preserve_default=True,
        ),
    ]
