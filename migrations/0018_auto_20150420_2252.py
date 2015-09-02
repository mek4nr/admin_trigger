# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0017_auto_20150420_2004'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForeignEvent',
            fields=[
                ('event_ptr', models.OneToOneField(primary_key=True, to='event.Event', auto_created=True, serialize=False, parent_link=True)),
                ('classname', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
            },
            bases=('event.event',),
        ),
        migrations.RemoveField(
            model_name='genericevent',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='genericevent',
            name='event_ptr',
        ),
        migrations.DeleteModel(
            name='GenericEvent',
        ),
    ]
