
from command_search import *

class FactorySearchFilter(object):

    def create_search_filter(self, searchOper):
        pass



class JqGridFactorySearchFilters(FactorySearchFilter):

    def create_search_filter(self, searchOper):

        if searchOper == 'eq': return EqualStringFilter()

        if searchOper == 'ne': return NotEqualStringFilter()

        if searchOper == 'bw': return BeginWithFilter()

        if searchOper == 'bn': return NotBeginWithFilter()

        if searchOper == 'ew': return EndWithFilter()

        if searchOper == 'en': return NotEndWithFilter()

        if searchOper == 'cn': return ContainFilter()

        if searchOper == 'nc': return NotContainFilter()

        if searchOper == 'lt': return LessThanFilter()

        if searchOper == 'le': return LessOrEqualThanFilter()

        if searchOper == 'gt': return GreaterThanFilter()

        if searchOper == 'ge': return GreaterOrEqualThanFilter()
