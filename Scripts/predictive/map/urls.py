
from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'index', views.index, name='index'),
        url(r'marker', views.marker, name='marker'),
        url(r'product', views.product, name='product'),
        url(r'init_main', views.init_main, name='init_main'),
        url(r'init_dist', views.init_dist, name='init_dist'),
        url(r'districts', views.districts, name='districts'),
        url(r'indDistricts', views.indDistricts, name='indDistricts'),
        url(r'region/(?P<district>([A-Z])\w+(\s)?(([A-Z])\w+)?(\s)?(([A-Z])\w+)?)', views.region, name='regions'),
        url(r'sms', views.sms, name='sms'),
        url(r'changedate', views.changedate, name='changedate'),
        url(r'hosp_overview', views.hosp_overview, name='hosp_overview'),
        url(r'dist_charts', views.dist_charts, name='dist_charts'),
        url(r'addcases', views.addcases, name='addcases'),
        url(r'about', views.about, name='about'),
        url(r'contact', views.contact, name='contact'),
        url(r'blog', views.blog, name='blog'),
        url(r'service', views.service, name='service'),
        url(r'hosp_overview', views.hosp_overview, name='hosp_overview'),

        url(r'dist_charts', views.dist_charts, name='dist_charts'),
        url(r'downloads', views.downloads, name='downloads'),
        url(r'reports', views.reports, name='reports'),
        url(r'country_charts', views.country_charts, name='country_charts')

    ]
