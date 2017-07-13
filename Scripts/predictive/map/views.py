from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers

from datetime import datetime as dt
from .models import Districts, Reports

def index(request):
    most_north = Districts.objects.order_by('-longitude')[:5]
    context = {'most_north':most_north}
    most_south = Districts.objects.order_by('longitude')[:5]
    context.update({'most_south':most_south})
    most_west = Districts.objects.order_by('latitude')[:5]
    context.update({'most_west':most_west})
    most_east = Districts.objects.order_by('-latitude')[:5]
    context.update({'most_east':most_east})
    return render(request, 'map/index.html', context)

def marker(request):
    lat, lng, date_string = round(float(request.GET.get('lat', None)),3), round(float(request.GET.get('lng', None)),3), request.GET.get('date')
    district = Districts.objects.filter(latitude=lat).filter(longitude=lng)
    context = {'district':district}
    Date = dt.strptime(date_string, '%Y-%m-%d')
    reports = Reports.objects.filter(date=Date).filter(district=district)
    context.update({'reports':reports})
    html = render(request, 'map/sidebar_data.html', context)
    return HttpResponse(html)
    
def product(request):
    districts = Districts.objects.all()
    districtdict = []    
    for district in districts:
        report = Reports.objects.filter(distict=district)
        corddict = {district.name : {'lat' : district.latitude, 'lng' : district.longitude, 'deaths' : report.death_cnfmd}}
        districtdict.update(corddict)
    return render(request, 'map/product.html', districtdict)

def init(request):
    data = {}
    districts = Districts.objects.all()
    i = 1
    for district in districts:
        data.update({'id' : i, 'fields' : {'name' : district.name, 'lat' : district.latitude, 'lng' : district.longitude}})
        i += 1
    print(data)
    return JsonResponse(data)
    
    
        
