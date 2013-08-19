from django.conf.urls import patterns, include, url
from django.contrib import admin

from views import test, get_customers

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^test/get_customers', get_customers),
    (r'^test/', test),
    (r'^', test),
)
