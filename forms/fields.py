# -*- coding: utf-8 -*-
"""
..module:forms.fields
    :project: smooth_perms
    :platform: Unix
    :synopsis: Module for custom fields, created on 05/02/2016

..moduleauthor:: Jean-Baptiste Munieres <jbaptiste.munieres@gmail.com>

"""
from django import forms
from admin_trigger.forms.widgets import SelectMultipleChosen


class MultipleChoiceFieldFields(forms.MultipleChoiceField):
    """
    Class MultipleChoiceFieldFields for select fields in SmoothRegistryModel,
    choice depend on parent so need valid in form
    """
    widget = SelectMultipleChosen

    def valid_value(self, value):
        return True