# -*- coding: utf-8 -*-
import csv
import codecs
from anytree import AnyNode, LevelOrderGroupIter
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models.manager import BaseManager
from django import forms
from django.db.models import ForeignKey
from django.db.models.fields import AutoField
from django.db.models.fields import BooleanField
from django.db.models.fields import CharField
from django.db.models.fields import DateField
from django.db.models.fields import DurationField
from django.db.models.fields import FilePathField
from django.db.models.fields import FloatField
from django.db.models.fields import IntegerField
from django.db.models.fields import IPAddressField
from django.db.models.fields import TextField
from django.db.models.fields import TimeField
from django.db.models.fields import BinaryField
from django.db.models.fields import UUIDField
from django.db.models.fields import GenericIPAddressField
from .forms import CSVFormatForm
from .forms import CSVFieldsForm
from .forms import CheckboxSelectAll


SUPPORTED_FIELDS = (
    AutoField,
    BooleanField,
    CharField,
    DateField,
    DurationField,
    FilePathField,
    FloatField,
    IntegerField,
    IPAddressField,
    TextField,
    TimeField,
    BinaryField,
    UUIDField,
    GenericIPAddressField
)


class Node(AnyNode):
    """
    Adding an unique key-field to the AnyNode-class.
    """
    @property
    def key(self):
        return '_'.join(n.model.__name__ for n in self.path)


class CSVData:
    """
    Simple replacement for the filelike-object passed to the csv-writer.
    """
    DELIMITER = ','
    ESCAPECHAR = '\\'
    QUOTECHAR = ''
    LINETERMINATOR = '\r\n'
    DOUBLEQUOTE = False

    def __init__(self):
        self.data = str()

    def write(self, data):
        self.data += data

    def __str__(self):
        return self.data


def get_fields(model):
    """
    Get all model fields that are subclasses of SUPPORTED_FIELDS.
    """
    fields = model._meta.get_fields()
    fields = [f for f in fields if any(issubclass(type(f), F) for F in SUPPORTED_FIELDS)]
    return fields


def get_rel_fields(model):
    """
    Get model fields that are subclasses of ForeignKey.
    """
    fields = model._meta.get_fields()
    fields = [f for f in fields if issubclass(type(f), ForeignKey)]
    return fields


def get_choices(node):
    """
    Get choice-tuples for a given model.
    """
    path = '.'.join(n.field.name for n in node.path[1:])
    fields = get_fields(node.model)
    return (('{}.{}'.format(path, f.name).lstrip('.'), f.name) for f in fields)


def get_form_field(node):
    label = ' -> '.join(n.model._meta.verbose_name for n in node.path)
    help_text = _('Which fields do you want to export?')
    return forms.MultipleChoiceField(
        label=label,
        help_text=help_text,
        widget=CheckboxSelectAll,
        choices=get_choices(node),
        required=False)


def get_value(item, choice):
    fields = choice.split('.')
    for field in fields:
        value = getattr(item, field)
        item = value
    return str(value)


def csvexport(modeladmin, request, queryset):
    """
    Admin-action to export items as csv-formatted data.
    """
    # initiate the csv-form
    if 'csvexport' in request.POST:
        format_form = CSVFormatForm(request.POST)
        fields_form = CSVFieldsForm(request.POST)
    else:
        format_form = CSVFormatForm()
        fields_form = CSVFieldsForm()

    # Get model-fields as form-fields
    form_fields = dict()
    model = modeladmin.model
    current_node = Node(model=model)
    form_fields[current_node] = get_form_field(current_node)

    n = 0
    depth = getattr(settings, 'CSV_EXPORT_REFERENCE_DEPTH', 3)
    while n < depth:
        n += 1
        for node in tuple(LevelOrderGroupIter(current_node.root))[-1]:
            for field in get_rel_fields(node.model):
                current_node = Node(model=field.related_model, field=field, parent=node)
                form_fields[current_node] =  get_form_field(current_node)


    # Add form-fields to form
    for node, form_field in form_fields.items():
        fields_form.fields[node.key] = form_field

    # generate csv-data from form-data
    if format_form.is_valid() and fields_form.is_valid():
        # get csv-format
        csv_format = dict()
        csv_format['delimiter'] = format_form.cleaned_data['delimiter'] or CSVData.DELIMITER
        csv_format['escapechar'] = format_form.cleaned_data['escapechar'] or CSVData.ESCAPECHAR
        csv_format['quotechar'] = format_form.cleaned_data['quotechar'] or CSVData.QUOTECHAR
        csv_format['doublequote'] = format_form.cleaned_data['doublequote'] or CSVData.DOUBLEQUOTE
        newline = format_form.cleaned_data['lineterminator'] or CSVData.LINETERMINATOR
        csv_format['lineterminator'] = codecs.decode(newline, 'unicode_escape')
        csv_format['quoting'] = csv.QUOTE_ALL if csv_format['quotechar'] else csv.QUOTE_NONE

        # use select-options as csv-header
        header = list()
        for node in form_fields.keys():
            header += list(fields_form.cleaned_data[node.key])

        # setup the csv-writer
        csv_data = CSVData()
        writer = csv.writer(csv_data, **csv_format)

        # write csv-header and -data
        writer.writerow(tuple(f for f in header))
        for item in queryset:
            writer.writerow(tuple(get_value(item, f) for f in header))

        # return csv-data as view or download
        if 'csvexport_view' in request.POST:
            content_type="text/plain;charset=utf-8"
        elif 'csvexport_download' in request.POST:
            content_type="text/comma-separated-values"
        return HttpResponse(csv_data, content_type=content_type)

    else:
        return render(request, 'csvexport/csvexport.html', {
            'objects': queryset.order_by('pk'),
            'format_form': format_form,
            'fields_form': fields_form,
            'title': _('CSV-Export')
            })
