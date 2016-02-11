from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.core.signals import request_started
from datetime import datetime
from django.db import transaction
from django.core.exceptions import ValidationError
from django.forms.models import fields_for_model


class EventError(Exception):
    pass


class Event(models.Model):
    name = models.CharField(max_length=100)
    done = models.BooleanField(default=False)

    def get_object(self):
        return None

    def apply_event(self):
        for change in self.eventchangefield_set.all():
            change.done_change()

        self.done = True
        self.save()

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()

    class Meta:
        verbose_name = _(u'Event')
        verbose_name_plural = _(u'Events')


class ForeignEvent(Event):
    classname = models.CharField(max_length=100, null=True, blank=True)
    foreign_key = None

    def __init__(self, *args, **kwargs):
        super(ForeignEvent, self).__init__(*args, **kwargs)
        if self.foreign_key is None:
            raise AttributeError(_(u"The foreign_key attribute is necessary"))

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.classname = self.__class__.__name__.lower()

        super(ForeignEvent, self).save(*args, **kwargs)

    def get_object(self):
        parent_event = getattr(self, self.classname)
        try:
            return getattr(parent_event, parent_event.foreign_key)
        except AttributeError as e:
            raise e


class EventChangeField(models.Model):
    event = models.ForeignKey(Event)

    parent_content_type = models.ForeignKey(ContentType, related_name="parent_content_type")
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    field = models.CharField(max_length=100)
    field_type = models.CharField(max_length=100)
    value = models.TextField()

    def done_change(self):
        try:
            setattr(self.content_object, self.field, self.parse_value())
            self.content_object.save()
        except AttributeError as e:
            print e

    def parse_value(self):
        t = fields_for_model(self.content_type.model_class())
        try:
            return t[self.field].clean(self.value)
        except ValidationError as e:
            print e

    class Meta:
        verbose_name = _(u'Change on done')
        verbose_name_plural = _(u'Changes on done')


class Trigger(models.Model):
    event = models.ForeignKey(Event)

    class Meta:
        abstract = True


class TriggerField(Trigger):
    resource_unit = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = _(u'Fields Trigger')
        verbose_name_plural = _(u'Fields Triggers')

    def P(self):
        pass

    def V(self):
        pass


class TriggerDate(Trigger):
    date = models.DateTimeField()

    class Meta:
        verbose_name = _(u'Date Trigger')
        verbose_name_plural = _(u'Date Triggers')

    def __str__(self):
        return str(self.date)


class TriggerObject(models.Model):
    fields_trigger = models.CharField(max_length=1000)

    def activate_semaphore(self):
        pass

    def free_semaphore(self):
        pass


def callback_event(sender, **kwargs):
    for e in Event.objects.filter(done=False):
        if len(e.triggerdate_set.filter(date__lte=datetime.now())) > 0:
            e.apply_event()


request_started.connect(callback_event)
