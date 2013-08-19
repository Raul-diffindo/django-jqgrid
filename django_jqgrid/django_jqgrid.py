from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models.loading import get_model
from django.utils import simplejson
from datetime import *
from django.utils import formats
from decimal import *
import unicodedata

from factory_search_filter import *


class django_jqgrid(object):

    def __init__(self, app_label, model_name, url, models_fields_selected = [], edit_url = '', table_id = '', div_id = '',
                 data_type = 'json', caption = ''):

        #App
        self.app = app_label

        # Model to work with jqgrid
        self.model = get_model(app_label, model_name)

        # Fields selected to work with jqgrid
        if models_fields_selected:
            self.fields = models_fields_selected
        else:
            self.fields = self.model._meta.get_all_field_names()

        self.url = url
        self.edit_url = edit_url
        self.table_id = table_id
        self.div_id = div_id
        self.data_type = data_type
        self.caption = caption


    def get_objects(self, page = 1, limit = '', sidx = '', sord = '', search = '', searchField = False,
                    searchOper = False, searchString = False):

        if sord.lower() == 'asc':
            sord = '-'
        elif sord.lower() == 'desc':
            sord = ''

        if search.lower() == 'true':
            all_objects = self.search_objects(searchField, searchOper, searchString)
        else:
            all_objects = self.model.objects.all()

        all_objects = all_objects.order_by(str(sord) + str(sidx))

        num_objects = all_objects.count()

        paginator = Paginator(all_objects, int(limit))

        try:
            objects_page = paginator.page(page)
        except (EmptyPage, InvalidPage):
            objects_page = paginator.page(paginator.num_pages)

        lines = []
        i = 1

        for row in objects_page.object_list:

            line = {
                "id" : row.id,
                "cell": [i, ]
            }

            for field in self.fields:
                line['cell'].append(row.field)

            lines.append(line)
            i += 1

        results = {'page': page, 'total': paginator.num_pages, 'records': num_objects, 'rows': lines}

        if self.data_type == 'xml':
            return self.__serialize_toxml(results)
        else:
            return simplejson.dumps(results, indent=4)


    #Private Method. Do not Touch!
    def __serialize_toxml(self, root):
        xml = ''
        for key in root.keys():
            if isinstance(root[key], dict):
                xml = '%s<%s>\n%s</%s>\n' % (xml, key, self.__serialize_toxml(root[key]), key)
            elif isinstance(root[key], list):
                xml = '%s<%s>' % (xml, key)
                for item in root[key]:
                    xml = '%s%s' % (xml, self.__serialize_toxml(item))
                xml = '%s</%s>' % (xml, key)
            else:
                value = root[key]
                xml = '%s<%s>%s</%s>\n' % (xml, key, value, key)
        return xml


    def search_objects(self, searchField, searchOper, searchString):

        filter = JqGridFactorySearchFilters().create_search_filter(searchOper)
        return filter.execute_query(self.app, self.model, searchField, searchString)


    def add_object(self, request):

        new_object = self.model()

        for field in self.fields:

            if request.POST.get(field) != '':
                data_type = self.model._meta.get_field(field).get_internal_type()
                new_object[field] = self.__rescue_convert_data(data_type, field, request)

        return new_object.save()


    def edit_object(self, object_id, request):

        object_for_update = self.model.objects.get(id = object_id)

        for field in self.fields:

            if request.POST.get(field) != '':
                data_type = self.model._meta.get_field(field).get_internal_type()
                object_for_update[field] = self.__rescue_convert_data(data_type, field, request)

        return object_for_update.save()


    def delete_object(self, object_id):
        try:
            self.model.objects.get(id = object_id).delete()
            return True
        except:
            return False

        
    #Private Method. Do not Touch!
    def __rescue_convert_data(self, data_type, field, request):

        if data_type in ['IntegerField', 'BigIntegerField', 'PositiveIntegerField', 'SmallIntegerField']:
                return int(request.POST.get(field))

        elif data_type in ['DecimalField']:
            return Decimal(request.POST.get(field))

        elif data_type in ['FloatField']:
            return float(request.POST.get(field))

        elif data_type in ['DateField', 'DateTimeField', 'TimeField']:
            return datetime.strptime(request.POST.get(field),
                                                  formats.date_format(field, "SHORT_DATETIME_FORMAT")),
        else:
            return request.POST.get(field)


    def get_colmodel(self):
        colModel = []

        for field in self.fields:
            colModel.append(self.__colmodel_of_field(field))

        return str(colModel)


    #Private Method. Do not Touch!
    def __colmodel_of_field(self, field):
        default_colModel = {
            'name': field.encode('ascii','ignore'),
            'index': field.encode('ascii','ignore'),
            'width': 100,
            'editable': 'true',
        }
        return default_colModel


    def get_colnames(self):
        colNames = []

        for field in self.fields:
            colNames.append(field.encode('ascii','ignore').capitalize())

        return str(colNames).encode('ascii', 'xmlcharrefreplace')


    def get_id_tablegrid(self):
        if not self.table_id == '': return self.table_id
        return self.app + '-' + self.model._meta.verbose_name_plural + '-grid'


    def get_id_divgrid(self):
        if not self.div_id == '': return self.div_id
        return self.app + '-' + self.model._meta.verbose_name_plural


    def get_edit_url(self):
        return self.edit_url


    def get_caption(self):
        if not self.caption == '': return self.caption
        return self.model._meta.verbose_name_plural


    def get_data_type(self):
        return self.data_type

