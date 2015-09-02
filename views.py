from django.http import HttpResponse
from event.admin import EventChangeFieldGenerator, generate_value, unparse_value
from django.contrib.contenttypes.models import ContentType
from django import forms
from django.contrib.auth.decorators import login_required
from tanuki.contants import mylog
from django.forms.models import fields_for_model
from event.models import Event
import json


def get_list_content_type(request, content_type_id):
    e = EventChangeFieldGenerator(request)
    content_type = ContentType.objects.get(id=content_type_id)
    return e.get_objects_tree(content_type)


def get_list_object(request, obj):
    e = EventChangeFieldGenerator(request)
    content_type, obj = unparse_value(obj)
    return e.get_fields_with_obj(obj)


@login_required
def get_objects_from_content_type(request, content_type_id):
    choices = get_list_content_type(request, content_type_id)
    return HttpResponse(forms.Select().render_options(choices, choices[0][0]))


@login_required
def get_fields_from_object(request, obj):
    choices = get_list_object(request, obj)
    return HttpResponse(forms.Select().render_options(choices, choices[0][0]))


@login_required
def get_formfield(request, obj, field):
    e = EventChangeFieldGenerator(request)
    content_type, obj = unparse_value(obj)

    # Get current value (don't process if an event will change before u or after)
    value = getattr(obj, field)
    fields = e.get_field(obj, field)
    t = fields_for_model(content_type.model_class())
    return HttpResponse(t[fields.name].widget.render(fields, value=value))


def process_event(request, num):
    event = Event.objects.get(id=num)
    event.apply_event()
    return HttpResponse("Page loaded")