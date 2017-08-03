from django.shortcuts import render

from django.http import HttpResponse
#from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
#from .fusioncharts import FusionCharts
import json
from django.core import management

from datetime import datetime as dt
from datetime import timedelta as td
from .models import Reports

#return the main map
def index(request):
    return HttpResponse(render(request, 'demo/index.html'))

#receive a text message and add the data to a database
@csrf_exempt
def sms(request):
#    message = request.POST.get('Body')
#    from_number = request.POST.get('From')
    message = "Ebola, 100"
    from_number = "+1232147755"
    if "," in message:
        if len(message.split(",")) > 2:
            start = message.find(",")
            disease = message[:start]
            count = message[start:].replace(",", "").strip()
            try:
                int(count)
            except 'ValueError':
                print("1")
                return HttpResponse('<h1>Bad</h1>')
        else:
            disease, count = message.split(",")[0], message.split(",")[1]
        try:
            count = int(count)
        except 'ValueError':
            print("2")
            return HttpResponse('<h1>Bad</h1>')
        if (count < 200) and (count > 0):
            try:
                management.call_command(
                        'add_phone',
                        disease,
                        count,
                        from_number
                    )
            except:
                print("3")
                return HttpResponse('<h1>Bad</h1>')
        else:
            print("Nice try")
    print("4")
    return HttpResponse('<h1>Nice</h1>')

def add_cases(request):

    #add all the data we've collected for today
    reportsdict ={}

    i = 0
    Date = dt.today()
    reports = Reports.objects.filter(date=Date)
    areas = []
    for report in reports:
        if report.phone_number.code.name_state not in areas:
            areas.append(report.phone_number.code.name_state)
    
    data = []
    for area in areas:
        report = reports.filter(phone_number__code__name_state=area)
        areaName = area
        lat = report.first().phone_number.code.lat
        lng = report.first().phone_number.code.lng
        case_count = report.aggregate(Sum('count'))['count__sum']
        data.append([areaName, lat, lng, case_count])
    
    data.sort(key=lambda x: x[3])
    j = len(data)
    for row in data:
        reportsdict.update({i : {'areaName': row[0], 'lat' : str(row[1]), 'lng' : str(row[2]), 'deaths' : str(row[3]), 'zval': str(j)}})
        i += 1
        j -= 1
    
    data = json.dumps(reportsdict)
    return HttpResponse(data, content_type="application/json")

def add_cases_refresh(request):

    #add all the data we've collected for today
    reportsdict ={}

    i = 0
    Date = dt.now() - td(seconds=60)
    reports = Reports.objects.filter(date__gte=Date)
    areas = []
    for report in reports:
        if report.phone_number.code.name_state not in areas:
            areas.append(report.phone_number.code.name_state)
    
    data = []
    for area in areas:
        report = reports.filter(phone_number__code__name_state=area)
        areaName = area
        lat = report.first().phone_number.code.lat
        lng = report.first().phone_number.code.lng
        case_count = report.aggregate(Sum('count'))['count__sum']
        data.append([areaName, lat, lng, case_count])
    
    data.sort(key=lambda x: x[3])
    j = len(data)
    for row in data:
        reportsdict.update({i : {'areaName': row[0], 'lat' : str(row[1]), 'lng' : str(row[2]), 'deaths' : str(row[3]), 'zval': str(j)}})
        i += 1
        j -= 1
    
    data = json.dumps(reportsdict)
    return HttpResponse(data, content_type="application/json")

def states(request):
    data = render(request, 'demo/states_outlines.html')
    return HttpResponse(data, content_type="application/json")

