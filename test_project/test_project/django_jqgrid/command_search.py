
from django.db.models import Q

#Interface for Filter
class AbstractFilter(object):

    def execute_query(self, app, model, searchField, searchString):
        pass


# Concretes Filters


#Equal comparision
class EqualStringFilter(AbstractFilter):

    def execute_query(self, app, model, searchField, searchString):
         return model.objects.filter(Q(**{ searchField + '__iexact' : searchString}))


#Not Equal comparision
class NotEqualStringFilter(AbstractFilter):

    def execute_query(self, app, model, searchField, searchString):
         return model.objects.exclude(Q(**{ searchField + '__iexact' : searchString}))


#String Begin with
class BeginWithFilter(AbstractFilter):

    def execute_query(self, app, model, searchField, searchString):
         return model.objects.filter(Q(**{ searchField + '__istartswith' : searchString}))


#String Not Begin with
class NotBeginWithFilter(AbstractFilter):

    def execute_query(self, app, model, searchField, searchString):
         return model.objects.exclude(Q(**{ searchField + '__istartswith' : searchString}))


#String End with
class EndWithFilter(AbstractFilter):

    def execute_query(self, app, model, searchField, searchString):
         return model.objects.filter(Q(**{ searchField + '__iendswith' : searchString}))


#String Not End with
class NotEndWithFilter(AbstractFilter):

    def execute_query(self, app, model, searchField, searchString):
         return model.objects.exclude(Q(**{ searchField + '__iendswith' : searchString}))


#String Contain
class ContainFilter(AbstractFilter):

    def execute_query(self, app, model, searchField, searchString):
         return model.objects.filter(Q(**{ searchField + '__icontains' : searchString}))


#String Not Contain
class NotContainFilter(AbstractFilter):

    def execute_query(self, app, model, searchField, searchString):
         return model.objects.exclude(Q(**{ searchField + '__icontains' : searchString}))


#Field Less Than...
class LessThanFilter(AbstractFilter):

    def execute_query(self, app, model, searchField, searchString):
         return model.objects.filter(Q(**{ searchField + '__lt' : searchString}))


#Field Less Than or Equal Than...
class LessOrEqualThanFilter(AbstractFilter):

    def execute_query(self, app, model, searchField, searchString):
         return model.objects.filter(Q(**{ searchField + '__lte' : searchString}))


#Field Greater Than...
class GreaterThanFilter(AbstractFilter):

    def execute_query(self, app, model, searchField, searchString):
         return model.objects.filter(Q(**{ searchField + '__gt' : searchString}))


#Field Greater or Equal Than...
class GreaterOrEqualThanFilter(AbstractFilter):

    def execute_query(self, app, model, searchField, searchString):
         return model.objects.filter(Q(**{ searchField + '__gte' : searchString}))

