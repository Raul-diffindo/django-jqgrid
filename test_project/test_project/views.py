from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_http_methods

from django_jqgrid.django_jqgrid import django_jqgrid

def test(request):

    my_django_jqgrid = django_jqgrid('app_test', 'Customer', '/test/get_customers', edit_url = '/test/edit_customer',
                                     data_type = 'json')

    context = {
        'jqgrid_table_id': my_django_jqgrid.get_id_tablegrid(),
        'jqgrid_div_id': my_django_jqgrid.get_id_divgrid(),
        'jqgrid_url': my_django_jqgrid.url,
        'jqgrid_datatype': my_django_jqgrid.get_data_type(),
        'jqgrid_colnames': my_django_jqgrid.get_colnames(),
        'jqgrid_colmodel': my_django_jqgrid.get_colmodel(),
        'jqgrid_caption': my_django_jqgrid.get_caption(),
        'jqgrid_edit_url': my_django_jqgrid.get_edit_url(),
    }

    context.update(csrf(request))
    return render_to_response('test.html', context, RequestContext(request))


@require_http_methods(["GET"])
def get_customers(request):
    my_django_jqgrid = django_jqgrid('app_test', 'Customer', '/test/get_customers', edit_url = '/test/edit_customer',
                                     data_type = 'json')


    return HttpResponse(my_django_jqgrid.get_objects(request.GET.get('page',''),
                                                    request.GET.get('rows', ''),
                                                    request.GET.get('sidx', ''),
                                                    request.GET.get('sord', ''),
                                                    request.GET.get('_search',''),
                                                    request.GET.get('searchField',''),
                                                    request.GET.get('searchOper',''),
                                                    request.GET.get('searchString',''),
                                                     ),
                        mimetype='application/json')
