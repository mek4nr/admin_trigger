# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import event.validators


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0012_triggerfield_event'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name_plural': 'Events', 'verbose_name': 'Event'},
        ),
        migrations.AlterModelOptions(
            name='eventchangefield',
            options={'verbose_name_plural': 'Changes on done', 'verbose_name': 'Change on done'},
        ),
        migrations.AlterModelOptions(
            name='triggerdate',
            options={'verbose_name_plural': 'Date Triggers', 'verbose_name': 'Date Trigger'},
        ),
        migrations.AlterModelOptions(
            name='triggerfield',
            options={'verbose_name_plural': 'Fields Triggers', 'verbose_name': 'Fields Trigger'},
        ),
        migrations.AddField(
            model_name='eventchangefield',
            name='field',
            field=models.CharField(max_length=100, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventchangefield',
            name='field_type',
            field=models.CharField(max_length=100, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventchangefield',
            name='value',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='triggerdate',
            name='date',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
    ]
