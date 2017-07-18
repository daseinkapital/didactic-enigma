
from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'marker', views.marker, name='marker'),
        url(r'product', views.product, name='product'),
        url(r'init', views.init, name='init'),
        url(r'districts', views.districts, name='districts')
    
    ]
