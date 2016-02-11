# -*- coding: utf-8 -*-
"""
..module:urls
    :project: 
    :platform: Unix
    :synopsis: Module for core database specification, created on 23/04/2015 

..moduleauthor:: Jean-Baptiste Munieres <jbaptiste.munieres@gmail.com>

"""
from django.conf.urls import patterns, include, url, static


urlpatterns = patterns(
    'admin_trigger.views',
    url(r'^objects/(?P<content_type_id>[0-9]+)/?$', 'get_objects_from_content_type'),
    url(r'^fields/(?P<obj>[0-9]+:[0-9]+)/?$', 'get_fields_from_object'),
    url(r'^field/(?P<obj>[0-9]+:[0-9]+)/(?P<field>.+)/?$', 'get_formfield'),
    #url(r'^process/(?P<num>[0-9]+)/?$', 'process_event'),
)
