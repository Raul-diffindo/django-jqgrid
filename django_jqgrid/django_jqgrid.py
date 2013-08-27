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


class DjangoJqgrid(object):

    """
    Class to manage jqGrid from Django
    """

    def __init__(self, app_label, model_name, url, models_fields_selected = [], edit_url = '', table_id = '', div_id = '',
                 data_type = 'json', caption = ''):
        """
        Create a new DjangoJqgrid class instance.

        app_lable is the name of the your django app wich you want manage with Django JqGrid.
        model_name is the name of the model wich you want manage with Django jqGrid.
        models_fields_selected if you want manage only some fields of the model.
        edit_url is the url to edit a object from jqGrid.
        table_id is the id of the table of your jqGrid.
        div_id is the id of the div of your jqGrid.
        data type to use for communicate with jqGrid. Can be json or xml for the moment.
        caption of your jqGrid.
        """
        #App
        self.app = app_label

        # Model to work with jqgrid
        self.model = get_model(app_label, model_name)

        # Fields selected to work with jqgrid
        if models_fields_selected:
            self.fields = models_fields_selected
        else:
            self.fields = self.model._meta.get_all_field_names()
            self.fields.remove(u'id')

        self.url = url
        self.edit_url = edit_url
        self.table_id = table_id
        self.div_id = div_id
        self.data_type = data_type
        self.caption = caption


    def get_objects(self, page = 1, limit = '', sidx = '', sord = '', search = '', searchField = False,
                    searchOper = False, searchString = False):
        """
        Return all or objects filtered from self.model.

        Page: indicate the page to return
        limit: get how many rows we want to have into the grid - rowNum parameter in the grid.
        sidx: get index row - i.e. user click to sort. At first time sortname parameter -
        after that the index from colModel.
        sord: sorting order - at first time sortorder.
        search: indicate if the request is a search request
        searchField if is a search request searchField indicate the field of the search.
        searchOper indicate the filter of the search.
        searchString indicate the text value is the entered by the user.
        """

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
                line['cell'].append(self.__convert_data(getattr(row, field)))

            lines.append(line)
            i += 1

        results = {'page': page, 'total': paginator.num_pages, 'records': num_objects, 'rows': lines}

        if self.data_type == 'xml':
            return self.__serialize_toxml(results)
        else:
            return simplejson.dumps(results, indent=4)



    #Private Method. Do not Touch!
    def __convert_data(self, field):
        """
        Convert some Django Model fields to visualization in jqGrid correctly
        """

        if type(field).__name__ in ['DateField', 'DateTimeField', 'TimeField']:
            return field.strftime(formats.date_format(field, "SHORT_DATETIME_FORMAT"))

        else:
            return str(field)



    #Private Method. Do not Touch!
    def __serialize_toxml(self, root):
        """
        Serialize the result of a method to xml exit.
        """
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
        """
        Search method. Rely on command_search and factory_search_filter for obtain the exactly filter to execute.
        Return the objects filtered from the model using searchField, searchOper and searchString values
        """

        filter = JqGridFactorySearchFilters().create_search_filter(searchOper)
        return filter.execute_query(self.app, self.model, searchField, searchString)


    def add_object(self, request):
        """
        jqGrid add method control. Add a new object into model.
        Return the new object created.
        """
        try:
            new_object = self.model()

            for field in self.fields:

                if request.POST.get(field) != '':
                    data_type = self.model._meta.get_field(field).get_internal_type()
                    setattr(new_object, field, self.__rescue_convert_data(data_type, field, request))

            new_object.save()
            return True

        except:
            return False


    def edit_object(self, object_id, request):
        """
        jqGrid edit method control. Edit an existing object of the model.
        Return the object edited.
        """
        try:
            object_for_update = self.model.objects.get(id = object_id)

            for field in self.fields:
                if request.POST.get(field) != '':
                    data_type = self.model._meta.get_field(field).get_internal_type()
                    setattr(object_for_update, field, self.__rescue_convert_data(data_type, field, request))

            object_for_update.save()
            return True

        except Exception as e:
            return False


    def delete_object(self, object_id):
        """
        Delete an object identified by id from model
        Return True or False if the oper has been accomplished
        """
        try:
            self.model.objects.get(id = object_id).delete()
            return True
        except:
            return False

        
    #Private Method. Do not Touch!
    def __rescue_convert_data(self, data_type, field, request):
        """
        Private method to convert data from jqGrid to model fields.
        """

        if data_type in ['IntegerField', 'BigIntegerField', 'PositiveIntegerField', 'SmallIntegerField']:
            try:
                return int(request.POST.get(field))
            except:
                return 0

        elif data_type in ['Decimal']:
            try:
                return Decimal(request.POST.get(field))
            except:
                return Decimal(0)

        elif data_type in ['Float']:
            try:
                return float(request.POST.get(field))
            except:
                return 0.0

        elif data_type in ['Date', 'DateTime', 'Time']:
            try:
                return datetime.strptime(request.POST.get(field),
                                        formats.date_format(field, "SHORT_DATETIME_FORMAT")),
            except:
                return datetime.utcnow()
        else:
            return request.POST.get(field)


    def get_colmodel(self):
        """
        From fields of model return the jqGrid colModel field.
        """
        colModel = [{'name':'id','index':'id','width':40, 'search': False, 'align':'center', 'editable': False,} ]

        for field in self.fields:
            colModel.append(self.__colmodel_of_field(field, self.model._meta.get_field(field).get_internal_type()))

        return self.__adjust_colmodel_string(colModel)


    def __adjust_colmodel_string(self, colModel):
        replace_list = [("'sopt'", "sopt")]
        colModel_string = str(colModel).lower()

        for replace in replace_list:
            colModel_string = colModel_string.replace(replace[0], replace[1])

        return colModel_string

    #Private Method. Do not Touch!
    def __colmodel_of_field(self, field, data_type):
        """
        Private method to compose one field of jqGrid colModel field.
        """
        default_colModel = {
            'name': field.encode('ascii','ignore'),
            'index': field.encode('ascii','ignore'),
            'width': 100,
            'editable': True,
        }

        search_options = self.__get_field_search_options(data_type)
        if search_options:
            default_colModel['search'] = True
            default_colModel['searchoptions'] = search_options
        else:
            default_colModel['search'] = False

        return default_colModel

    def __get_field_search_options(self, data_type):
        """
        Private method to get the search options string for a field type.
        """
        if data_type in ['IntegerField', 'BigIntegerField', 'PositiveIntegerField', 'SmallIntegerField',
                         'DateField', 'DateTimeField', 'TimeField', 'DecimalField', 'FloatField']:
            return {"sopt":["eq", "ne", "lt", "le", "gt", "ge"]}
        elif data_type in ['CharField']:
            return {"sopt":["bw", "bn", "in", "ni", "ew", "en", "cn", "nc"]}
        else:
            return None


    def get_colnames(self):
        """
        Return the jqGrid colNames field from model fields.
        """
        colNames = ['N']

        for field in self.fields:
            colNames.append(field.encode('ascii','ignore').capitalize())

        return str(colNames).encode('ascii', 'xmlcharrefreplace')


    def get_id_tablegrid(self):
        """
        Return the jqGrid table id. If it is None return app-model-grid
        """
        if not self.table_id == '': return self.table_id
        return self.app + '-' + self.model._meta.verbose_name_plural + '-grid'


    def get_id_divgrid(self):
        """
        Return the jqGrid div id. If it is None return app-model
        """
        if not self.div_id == '': return self.div_id
        return self.app + '-' + self.model._meta.verbose_name_plural


    def get_edit_url(self):
        """
        Return the edit url for this jqGrid. We could use the special method __getitem__ too.
        """
        return self.edit_url


    def get_caption(self):
        """
        Return the Caption for this jqGrid. By default the caption is Model verbose plurar name.
        """
        if not self.caption == '': return self.caption
        return self.model._meta.verbose_name_plural


    def get_data_type(self):
        """
        Return the data type for this jqGrid. We could use the special method __getitem__ too.
        """
        return self.data_type

