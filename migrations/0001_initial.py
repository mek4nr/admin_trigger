# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('done', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
        migrations.CreateModel(
            name='EventChangeField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('field', models.CharField(max_length=100)),
                ('field_type', models.CharField(max_length=100)),
                ('value', models.TextField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Change on done',
                'verbose_name_plural': 'Changes on done',
            },
        ),
        migrations.CreateModel(
            name='TriggerDate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Date Trigger',
                'verbose_name_plural': 'Date Triggers',
            },
        ),
        migrations.CreateModel(
            name='TriggerField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('resource_unit', models.PositiveIntegerField(default=1)),
            ],
            options={
                'verbose_name': 'Fields Trigger',
                'verbose_name_plural': 'Fields Triggers',
            },
        ),
        migrations.CreateModel(
            name='TriggerObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fields_trigger', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='ForeignEvent',
            fields=[
                ('event_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='admin_trigger.Event')),
                ('classname', models.CharField(max_length=100, null=True, blank=True)),
            ],
            bases=('admin_trigger.event',),
        ),
        migrations.AddField(
            model_name='triggerfield',
            name='event',
            field=models.ForeignKey(to='admin_trigger.Event'),
        ),
        migrations.AddField(
            model_name='triggerdate',
            name='event',
            field=models.ForeignKey(to='admin_trigger.Event'),
        ),
        migrations.AddField(
            model_name='eventchangefield',
            name='event',
            field=models.ForeignKey(to='admin_trigger.Event'),
        ),
        migrations.AddField(
            model_name='eventchangefield',
            name='parent_content_type',
            field=models.ForeignKey(related_name='parent_content_type', to='contenttypes.ContentType'),
        ),
    ]
