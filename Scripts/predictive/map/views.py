from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
import json

from math import log, ceil as log, ceil
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
    most_north = Districts.objects.order_by('-longitude')[:5]
    context = {'most_north':most_north}
    return render(request, 'map/product.html', context)

def init(request):
    districts = Districts.objects.all()
    districtdict = {} 
    i = 0
    for district in districts:
        report = Reports.objects.filter(district=district).first()
        if report.death_cnfmd != 0:
            corddict = {i : {'lat' : str(district.latitude), 'lng' : str(district.longitude), 'deaths' : str(ceil((log(report.death_cnfmd)/4)/log(4)))}}
        else:
            corddict = {i : {'lat' : str(district.latitude), 'lng' : str(district.longitude), 'deaths' : str(report.death_cnfmd)}}            
        districtdict.update(corddict)
        i += 1;
    data = json.dumps(districtdict)
    return HttpResponse(data, content_type="application/json")

def districts(request):
    data = render(request, 'map/jsonResponse.html')
    return HttpResponse(data, content_type="application/json")

def region(request, district):
    return render(request, 'map/region.html', {'district_name' : district})
        
