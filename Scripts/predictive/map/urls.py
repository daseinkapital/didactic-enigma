from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'marker', views.marker, name='marker'),
        url(r'product', views.product, name='product'),
        url(r'zoom', views.zoom, name='zoom')
    ]