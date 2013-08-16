from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models.loading import get_model
from django.utils import simplejson
from datetime import *
from django.utils import formats
from decimal import *

from factory_search_filter import *


class django_jqgrid(object):

    def __init__(self, app_label, model_name, models_fields_selected = []):

        #App
        self.app = app_label

        # Model to work with jqgrid
        self.model = get_model(app_label, model_name)

        # Fields selected to work with jqgrid
        if models_fields_selected:
            self.fields = models_fields_selected
        else:
            self.fields = self.model._meta.get_all_field_names()


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
        return simplejson.dumps(results, indent=4)



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