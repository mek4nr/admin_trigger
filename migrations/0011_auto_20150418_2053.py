# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0010_auto_20150418_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='triggerdate',
            name='date',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
    ]
