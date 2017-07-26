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
    districtName, date_string = request.GET.get('name'),request.GET.get('date')
    district = Districts.objects.filter(name=districtName)
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

def init_main(request):
    districts = Districts.objects.all()
    districtdict = {} 
    i = 0
    date = dt.strptime("2014-09-18","%Y-%m-%d")
    size_scale = [10, 100, 1000, 10000]
    for district in districts:
        report = Reports.objects.filter(district=district).filter(date = date).first()
        s = 1
        for size in size_scale:
            if report.death_cnfmd > size:
                s += 1
            else:
                break
        corddict = {i : {'name': district.name, 'lat' : str(district.latitude), 'lng' : str(district.longitude), 'deaths' : str(report.death_cnfmd), 'size' : s}}
        districtdict.update(corddict)
        i += 1
    data = json.dumps(districtdict)
    return HttpResponse(data, content_type="application/json")

def init_dist(request):
    dist_name = request.GET.get('name')
    districts = Districts.objects.filter(name=dist_name).first()
    map_data = {'zoom' : 10, 'lat' : str(districts.latitude), 'lng' : str(districts.longitude)}
    data = json.dumps(map_data)
    return HttpResponse(data, content_type="application/json")

def districts(request):
    data = render(request, 'map/jsonResponse.html')
    return HttpResponse(data, content_type="application/json")

def indDistricts(request):
    data = render(request, 'map/districtJson.html')
    return HttpResponse(data, content_type="application/json")

def region(request, district):
    return render(request, 'map/region.html', {'district_name' : district})

def changedate(request):
    startDate, endDate = dt.strptime(request.GET.get('startdate'), '%Y-%m-%d'), dt.strptime(request.GET.get('enddate'), '%Y-%m-%d')
    print(startDate)
    districts = Districts.objects.all()
    districtdict = {} 
    i = 0
    size_scale = [10, 100, 1000, 10000]
    for district in districts:
        report = Reports.objects.filter(district=district).filter(date__gte=startDate).first()
        if report:
            s = 1
            for size in size_scale:
                if report.death_cnfmd > size:
                    s += 1
                else:
                    break
            corddict = {i : {'name': district.name, 'lat' : str(district.latitude), 'lng' : str(district.longitude), 'deaths' : str(report.death_cnfmd), 'size' : s}}
            districtdict.update(corddict)
            i += 1
    data = json.dumps(districtdict)
    return HttpResponse(data, content_type="application/json")
    
        
