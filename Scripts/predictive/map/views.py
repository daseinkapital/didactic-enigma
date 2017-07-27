from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, Sum
import json

from datetime import datetime as dt
from .models import Districts, HeadReports, DeathReports


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
    context = {'district':districtName}
    Date = dt.strptime(date_string, '%Y-%m-%d')
    headReports = HeadReports.objects.filter(date=Date).filter(phone_number__hospital__district=district).aggregate(Sum('count'))
    deathReports = DeathReports.objects.filter(date=Date).filter(phone_number__hospital__district=district)
    context.update({'reports': headReports['count__sum']})
    print(context)
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
    Date = dt.strptime("2014-09-18","%Y-%m-%d")
    size_scale = [10, 100, 1000, 10000]
    for district in districts:
        report = HeadReports.objects.filter(date=Date).filter(phone_number__hospital__district=district)
        s = 1
        for size in size_scale:
            if report.count() > size:
                s += 1
            else:
                break
        corddict = {i : {'name': district.name, 'lat' : str(district.lat), 'lng' : str(district.lng), 'deaths' : str(report.count()), 'size' : s}}
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

@csrf_exempt
def sms(request):
    message = request.POST.get('Body')
    from_number = request.POST.get('From')
    print(message)
    print(from_number)
    return HttpResponse('<h1>Nice</h1>')
    
def changedate(request):
    startDate, endDate = dt.strptime(request.GET.get('startdate'), '%Y-%m-%d'), dt.strptime(request.GET.get('enddate'), '%Y-%m-%d')
    print(startDate)
    districts = Districts.objects.all()
    districtdict = {} 
    i = 0
    size_scale = [10, 100, 1000, 10000]
    for district in districts:
        report = HeadReports.objects.filter(date__gte=startDate).filter(phone_number__hospital__district=district)
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
