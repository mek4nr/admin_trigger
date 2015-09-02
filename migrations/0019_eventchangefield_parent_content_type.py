# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('event', '0018_auto_20150420_2252'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventchangefield',
            name='parent_content_type',
            field=models.ForeignKey(related_name='parent_content_type', to='contenttypes.ContentType', default=50),
            preserve_default=False,
        ),
    ]
