# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('event', '0014_event_classname'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForeignEvent',
            fields=[
                ('event_ptr', models.OneToOneField(serialize=False, primary_key=True, to='event.Event', parent_link=True, auto_created=True)),
            ],
            options={
            },
            bases=('event.event',),
        ),
        migrations.CreateModel(
            name='GenericEvent',
            fields=[
                ('event_ptr', models.OneToOneField(serialize=False, primary_key=True, to='event.Event', parent_link=True, auto_created=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=('event.event',),
        ),
        migrations.RemoveField(
            model_name='event',
            name='classname',
        ),
    ]
