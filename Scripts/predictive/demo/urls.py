
from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'sms', views.sms, name='sms'),
        url(r'add_cases', views.add_cases, name='add_cases'),
        url(r'add_cases_refresh', views.add_cases_refresh, name='add_cases_refresh'),
        url(r'states', views.states, name='states'),
        url(r'graph', views.graphs, name='graphs'),
        url(r'reports', views.reports, name='reports')
    ]
