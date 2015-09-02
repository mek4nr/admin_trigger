# -*- coding: utf-8 -*-
"""
..module:script
    :project: 
    :platform: Unix
    :synopsis: Module for core database specification, created on 21/04/2015 

..moduleauthor:: Jean-Baptiste Munieres <jbaptiste.munieres@gmail.com>

"""


class BaseFormSet(object):
    def __init__(self):
        print("BaseFormSet")
        self.test()

    def test(self):
        print("test")


class BaseModelFormSet(BaseFormSet):
    def __init__(self):
        print("BaseModelFormSet")
        super().__init__()


class BaseInlineFormSet(BaseModelFormSet):
    def __init__(self):
        print("BaseInlineFormSet")
        super().__init__()


class MyBaseModelFormSet(BaseFormSet):
    def __init__(self):
        print("MyBaseModelFormSet")
        super().__init__()


class MyBaseInlineFormSet(MyBaseModelFormSet):
    def __init__(self):
        print("MyBaseInlineFormSet")
        super().__init__()


class EventChangeFieldFormSetAdmin(MyBaseInlineFormSet, BaseInlineFormSet):
    def __init__(self):
        print("EventChangeFieldFormSetAdmin")
        super().__init__()

    def test(self):
        print("lol")


EventChangeFieldFormSetAdmin()