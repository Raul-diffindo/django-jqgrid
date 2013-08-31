import sys
from decimal import *
from datetime import *
import dateutil.parser
from django.utils import formats
from django.db.models import Q

#Dispathcer
class FieldDispatcher(object):

    _relationship_fields = ['ForeignKey']

    def convert_field_to_js(self, model, field, data_type, field_value):
        try:
            field_class = getattr(sys.modules[__name__], data_type)
            if not data_type in self._relationship_fields:
                return field_class().convert_field_to_js(field_value)
            else:
                return field_class().convert_field_to_js(model, field, field_value)
        except Exception as e:
            raise NotImplementedError(e)


    def convert_field_to_model(self, model, field, data_type, field_value):
        try:
            field_class = getattr(sys.modules[__name__], data_type)
            if not data_type in self._relationship_fields:
                return field_class().convert_field_to_model(field_value)
            else:
                return field_class().convert_field_to_model(model, field, field_value)
        except Exception as e:
            assert False, e
            raise NotImplementedError(e)


    def get_search_options(self, data_type):
        try:
            field_class = getattr(sys.modules[__name__], data_type)
            return field_class().get_search_options()
        except Exception as e:
            raise NotImplementedError(e)


######################### Design Pattern ###########################

#Interface:

class Field(object):

    def convert_field_to_js(self, field_value):
        pass

    def convert_field_to_model(self, field_value):
        pass

    def get_search_options(self):
        pass


#Interface Relationship Fields:
class RelationShipField(object):

    def convert_field_to_js(self, model, field, field_value):
        pass

    def convert_field_to_model(self, model, field, field_value):
        pass

    def get_search_options(self):
        pass


#Concrete Fields:

class IntegerField(Field):

    def convert_field_to_js(self, field_value):
        return str(field_value)

    def convert_field_to_model(self, value):
        try:
            return int(value)

        except Exception as e: raise ValueError(e)

    def get_search_options(self):
        return {"sopt":["eq", "ne", "lt", "le", "gt", "ge"]}


class BigIntegerField(Field):

    def convert_field_to_js(self, field_value):
        return str(field_value)

    def convert_field_to_model(self, value):
        try:
            return int(value)

        except Exception as e: raise ValueError(e)

    def get_search_options(self):
        return {"sopt":["eq", "ne", "lt", "le", "gt", "ge"]}


class PositiveIntegerField(Field):

    def convert_field_to_js(self, field_value):
        return str(field_value)

    def convert_field_to_model(self, value):
        try:
            return int(value)

        except Exception as e: raise ValueError(e)

    def get_search_options(self):
        return {"sopt":["eq", "ne", "lt", "le", "gt", "ge"]}


class SmallIntegerField(Field):

    def convert_field_to_js(self, field_value):
        return str(field_value)

    def convert_field_to_model(self, value):
        try:
            return int(value)

        except Exception as e: raise ValueError(e)

    def get_search_options(self):
        return {"sopt":["eq", "ne", "lt", "le", "gt", "ge"]}


class DecimalField(Field):

    def convert_field_to_js(self, field_value):
        return str(field_value)

    def convert_field_to_model(self, value):
        try:
            return Decimal(value)

        except Exception as e: raise InvalidOperation(e)

    def get_search_options(self):
        return {"sopt":["eq", "ne", "lt", "le", "gt", "ge"]}


class FloatField(Field):

    def convert_field_to_js(self, field_value):
        return str(field_value)

    def convert_field_to_model(self, value):
        try:
            return float(value)

        except Exception as e: raise ValueError(e)

    def get_search_options(self):
        return {"sopt":["eq", "ne", "lt", "le", "gt", "ge"]}


class DateField(Field):

    def convert_field_to_js(self, field_value):
        try:
            return field_value.strftime(formats.date_format(field_value, "SHORT_DATETIME_FORMAT"))

        except Exception as e: raise ValueError(e)

    def convert_field_to_model(self, field_value):
        try:
            return dateutil.parser.parse(field_value)

        except Exception as e: raise ValueError(e)

    def get_search_options(self):
        return {"sopt":["eq", "ne", "lt", "le", "gt", "ge"]}


class TimeField(Field):

    def convert_field_to_js(self, field_value):
        try:
            return field_value.strftime(formats.date_format(field_value, "SHORT_DATETIME_FORMAT"))

        except Exception as e: raise ValueError(e)

    def convert_field_to_model(self, field_value):
        try:
            return dateutil.parser.parse(field_value)

        except Exception as e: raise ValueError(e)

    def get_search_options(self):
        return {"sopt":["eq", "ne", "lt", "le", "gt", "ge"]}


class DateTimeField(Field):

    def convert_field_to_js(self, field_value):
        try:
            return field_value.strftime(formats.date_format(field_value, "SHORT_DATETIME_FORMAT"))

        except Exception as e: raise ValueError(e)

    def convert_field_to_model(self, field_value):
        try:
            return dateutil.parser.parse(field_value)

        except Exception as e: raise ValueError(e)

    def get_search_options(self):
        return {"sopt":["eq", "ne", "lt", "le", "gt", "ge"]}


class CharField(Field):

    def convert_field_to_js(self, field_value):
        try:
            return str(field_value)

        except Exception as e: raise ValueError(e)

    def convert_field_to_model(self, field_value):
        try:
            return str(field_value)

        except Exception as e: raise ValueError(e)

    def get_search_options(self):
        return {"sopt":["bw", "bn", "in", "ni", "ew", "en", "cn", "nc"]}


class TextField(Field):

    def convert_field_to_js(self, field_value):
        try:
            return str(field_value)

        except Exception as e: raise ValueError(e)

    def convert_field_to_model(self, field_value):
        try:
            return str(field_value)

        except Exception as e: raise ValueError(e)

    def get_search_options(self):
        return {"sopt":["bw", "bn", "in", "ni", "ew", "en", "cn", "nc"]}


class BooleanField(Field):

    _affirmative_response = 'Yes'
    _negative_response = 'No'
    _list_affirmative_responses = ['yes', 'si', 'oui', 'da', 'ja']

    def convert_field_to_js(self, field_value):
        if field_value: return self._affirmative_response
        else: return self._negative_response

    def convert_field_to_model(self, field_value):
        if field_value.lower() in self._list_affirmative_responses: return True
        else: return False

    def get_search_options(self):
        return {"sopt":["eq", "ne", ]}


#Concrete Relationship Fields

class ForeignKey(RelationShipField):

    def convert_field_to_js(self, model, field, field_value):
        try:
            return getattr(model.objects.filter(Q(**{ field : field_value}))[0], field).__unicode__()

        except Exception as e: raise ValueError(e)


    def convert_field_to_model(self, model, field, field_value):
        try:
            return model._meta.get_field(field).rel.to.objects.get(
                Q(**{ model._meta.get_field(field).rel.to._meta.jqgrid_related_field : field_value})
            )

        except Exception as e: raise ValueError(e)

    def get_search_options(self):
        return {"sopt":["eq", "ne", ]}