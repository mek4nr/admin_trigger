from admin_trigger.models import TriggerDate, EventChangeField, Event
from django import forms
from django.forms.models import BaseInlineFormSet
from django.contrib import admin
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.db.models import ForeignKey
from django.core.exceptions import ValidationError
from django.db import models


class ChoiceFieldObject(forms.ChoiceField):
    """
    Class ChoiceField for our custom field who good value is content_type_id:object_id
    """

    def valid_value(self, value):
        try:
            t = value.split(":")
            int(t[0])
            int(t[1])
            return True
        except Exception:
            return False


class ChoiceFieldField(forms.ChoiceField):
    """
    Class for list of valid fields, the value alone can't be validate, so validation must be in
    clean on ModelAdmin
    """
    def valid_value(self, value):
        return True


def generate_value(obj_id, content_type_id):
    """
    Function who parse obj & content_type for tree of objects
    :param obj_id: id of the object
    :param content_type_id: id of content_type
    :return: The value of content_type + object_id in string
    """
    return "{}:{}" . format(content_type_id, obj_id)


def unparse_value(value):
    """
    Function for unparse what generate_value parse
    :param value: The string value of content_type:object
    :return: ContentType, Object
    """
    t = value.split(":")
    try:
        c = ContentType.objects.get(id=t[0])
    except models.ObjectDoesNotExist as e:
        raise e

    try:
        return c, c.model_class().objects.get(id=t[1])
    except models.ObjectDoesNotExist as e:
        raise e


class EventChangeFieldGenerator(object):
    """
    Class who do all job for Event (list / content_type, tree object, fields)
    """

    def __init__(self, request):
        self.request = request

    @staticmethod
    def generate_content_type(content_type):
        """
        Function who take id or content_type object
        :param content_type: id or content_type object
        :return: ContentType
        """
        if isinstance(content_type, ContentType):
            return content_type
        elif isinstance(content_type, int):
            return ContentType.objects.get(id=content_type)

        raise models.ObjectDoesNotExist(_(u"The content_type giver isn't correct"))

    @staticmethod
    def generate_object(obj, content_type=None):
        """
        Function for get obj, take an obj or id & content_type
        :param obj: the object or id
        :param content_type: the content_type if object's id
        :return: ModelObject
        """
        if isinstance(obj, models.Model):
            return obj
        elif isinstance(content_type, ContentType) and isinstance(obj, int):
            return content_type.model_class().objects.get(id=obj)

        raise models.ObjectDoesNotExist(_(u"The obj given isn't correct"))

    @staticmethod
    def generate_choice(obj, content_type, level=0):
        """
        Function for generate choice in list of object
        :param obj: ModelObject
        :param content_type: ContentType
        :param level: level of nested
        :return: return lis
        """
        return [[generate_value(obj.id, content_type.id), "{} {}:{}" . format("--"*level, obj._meta.verbose_name, str(obj))]]

    def get_objects_tree(self, content_type):
        """
        Create a "tree" for all object and sub object (inline declared in admin) of content_type
        :param content_type: ContentType
        :return: list in tree of objects
        """
        choices = list()
        content_type = self.generate_content_type(content_type)
        all_obj = content_type.model_class().objects.all()

        try:
            admin_class = admin.site._registry[content_type.model_class()]

            for obj in all_obj:
                if admin_class.has_change_permission(request=self.request, obj=obj):
                    inlines = admin_class.get_inline_instances(self.request, obj)
                    choices += self.generate_choice(obj, content_type)
                    if len(inlines) > 0:
                        for inline in inlines:
                            choices += self.get_children_tree(inline, obj)
        except Exception as e:
            print e
        finally:
            return choices

    def get_children_tree(self, inline, parent, level=1):
        """
        Get object tree for level given
        :param inline: The inlineAdmin object
        :param parent: The parent modeladmin
        :param level: the current level of nest
        :return: a lest of tree object
        """
        model = inline.model
        content_type = ContentType.objects.get_for_model(model)
        choices = list()
        try:
            inlines = inline.inlines
        except Exception:
            inlines = []

        for f in model._meta.fields:
            if isinstance(f, ForeignKey):
                all_children = model.objects.filter(**{f.name: parent})
                for obj in all_children:
                    if inline.has_change_permission(request=self.request, obj=obj):
                        choices += self.generate_choice(obj, content_type, level)
                        if len(inlines) > 0:
                            for inline in inlines:
                                choices += self.get_children_tree(inline, obj, level+1)
        return choices

    def get_fields_with_obj(self, obj):
        """
        Get fields of object given
        :param obj: ModelObject
        :return: choices list of (field, verbose_name)
        """
        choices = list()
        fields = obj._meta.concrete_fields
        try:
            fields_admin = admin.site._registry[type(obj)].get_fields(self.request, obj)
            read_only_admin = admin.site._registry[type(obj)].get_readonly_fields(self.request, obj)
        except (AttributeError, KeyError, NameError):
            fields_admin = [field.name for field in fields]
            read_only_admin = []

        for field in fields:
            if field.name in ("id", "created_at", "modified_at", "owner"):
                continue
            if field.name in fields_admin and field.name not in read_only_admin:
                choices += [[field.name, field.verbose_name]]
        return choices

    def get_content_type_queryset(self, qs):
        """
        Exclude from the qs of ContentType, all one who user doesn't have permission or is not register
        :param qs: QuerySet of ContentType
        :return: QuerySet of ContentType
        """
        my_list = list(qs)
        for i, item in enumerate(my_list):
            all_obj = item.model_class().objects.all()
            try:
                admin_obj = admin.site._registry[item.model_class()]
                if len(all_obj) == 0:
                    qs = qs.exclude(id=item.id)
                else:
                    if not admin_obj.has_change_permission(request=self.request):
                        qs = qs.exclude(id=item.id)
                    else:
                        ok = False
                        for obj in all_obj:

                            if admin_obj.has_change_permission(request=self.request, obj=obj):
                                ok = True

                        if not ok:
                            qs = qs.exclude(id=item.id)
            except (AttributeError, KeyError, NameError):
                qs = qs.exclude(id=item.id)

        return qs

    def get_field(self, obj, field):
        """
        Get modelfield with name of this field
        :param obj: ModelObject
        :param field: Name of field
        :return: Field of ModelObject
        """
        for f in obj._meta.concrete_fields:
            if f.name == field:
                return f

    def valid_object(self, value, content_type):
        """
        Valid object with value return by form and ContentType
        :param value:
        :param content_type:
        :return:
        """
        choices = self.get_objects_tree(content_type)

        for val in choices:
            if val[0] == value:
                return True

        return False

    def valid_field(self, value, obj):
        """
        Valid field with value return by form and Object
        :param value:
        :param obj:
        :return:
        """
        choices = self.get_fields_with_obj(obj)

        for val in choices:
            if val[0] == value:
                return True

        return True


class EventChangeFieldFormAdmin(forms.ModelForm):
    object_custom = ChoiceFieldObject(label=_(u'Object'), choices=(('--', '-------'),),
                                      widget=forms.Select(
                                          attrs={'class': 'object_id-selector', 'style': 'max-width:300px',
                                                 'onchange': "object_change($(this).attr('id').split(new RegExp('-[A-Za-z_]*$'))[0])"}))
    value_custom = forms.CharField(label=_(u'Value'), required=False)

    class Meta:
        fields = ['parent_content_type', 'object_custom', 'field', 'field_type', 'value']
        exclude = ['content_type', 'object_id']
        widgets = {
            'parent_content_type': forms.Select(attrs={'class': 'content_type-selector',
                                                       'onchange': "content_type_change($(this).attr('id').split(new RegExp('-[A-Za-z_]*$'))[0])"}),
            'value': forms.HiddenInput(),
            'field_type': forms.HiddenInput(),
        }

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, **kwargs):
        self.request = kwargs.pop('request', None)
        super(EventChangeFieldFormAdmin, self).__init__(data, files, auto_id, prefix, initial, **kwargs)

        self.fields['field'] = ChoiceFieldField(choices=(('--', '-------'),),
                                                widget=forms.Select(
                                                    attrs={'class': 'field-selector',
                                                           'onchange': "field_change($(this).attr('id').split(new RegExp('-[A-Za-z_]*$'))[0])"}))

        self.e = EventChangeFieldGenerator(self.request)
        qs_parent = self.fields['parent_content_type'].queryset

        if self.instance.pk is not None:
            self.fields['object_custom'].choices = self.e.get_objects_tree(qs_parent.get(id=self.instance.parent_content_type.id))
            self.initial['object_custom'] = generate_value(self.instance.object_id, self.instance.content_type.id)
            self.fields['field'].choices = self.e.get_fields_with_obj(self.instance.content_object)

        self.fields['parent_content_type'].queryset = self.e.get_content_type_queryset(qs_parent)

    def clean(self):
        field = self.cleaned_data['field']
        parent_content_type = self.cleaned_data['parent_content_type']

        try:
            content_type, obj = unparse_value(self.cleaned_data['object_custom'])
        except models.ObjectDoesNotExist:
            raise ValidationError(_(u'Content type or object incorrect'))

        if not self.e.valid_object(self.cleaned_data['object_custom'], parent_content_type):
            raise ValidationError(_(u"You don't have permission for this object"))

        # Search if object have this field
        try:
            getattr(obj, field)
        except Exception:
            raise ValidationError(_(u"The field doesn't exist for this object"))

        if not self.e.valid_field(field, obj):
            raise ValidationError(_(u"You don't have permission for this field"))

    def save(self, commit=True):
        self.instance.content_type, obj = unparse_value(self.cleaned_data['object_custom'])
        self.instance.object_id = obj.id
        super(EventChangeFieldFormAdmin, self).save(commit)


class EventChangeFieldFormSetAdmin(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(EventChangeFieldFormSetAdmin, self).__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs['request'] = self.request
        return super(EventChangeFieldFormSetAdmin, self)._construct_form(i, **kwargs)

    @property
    def empty_form(self):
        form = self.form(
            auto_id=self.auto_id,
            prefix=self.add_prefix('__prefix__'),
            empty_permitted=True,
            request=self.request,
        )
        self.add_fields(form, None)
        return form


class EventChangeInlineAdmin(admin.TabularInline):
    form = EventChangeFieldFormAdmin
    formset = EventChangeFieldFormSetAdmin
    model = EventChangeField
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):

        AdminForm = super(EventChangeInlineAdmin, self).get_formset(request, obj, **kwargs)

        class AdminFormWithRequest(AdminForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return AdminForm(*args, **kwargs)

        return AdminFormWithRequest

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True


class TriggerDateInlineAdmin(admin.TabularInline):
    model = TriggerDate
    extra = 0

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    readonly_fields = ['done']
    inlines = [EventChangeInlineAdmin, TriggerDateInlineAdmin]

    class Media:
        js = (
            'js/object_id_selector.js',
        )

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True
