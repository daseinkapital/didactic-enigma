from django.shortcuts import render

from django.http import HttpResponse
#from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from time import sleep
from map.fusioncharts import FusionCharts
import json
from django.core import management
from datetime import datetime as dt
from .models import Reports, Phones

#return the main map
def index(request):
    return HttpResponse(render(request, 'demo/index.html'))

#receive a text message and add the data to a database
@csrf_exempt
def sms(request):
    message = request.POST.get('Body')
    from_number = request.POST.get('From')
    print(from_number)
    print(message)
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
        if (count < 201) and (count > 0):
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
    Date = dt.today()
    reports = Reports.objects.filter(date=Date)
    print(reports.count())
    print('Hello')
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

def graphs(request):
    sleep(4)    
    dataSource = {}
    
    dataSource["chart"] = {
        "caption": "Top 5 Diseases",
        "subCaption": "United States of America",
        "xAxisName": "Disease",
        "yAxisName": "Case Reports",
        "theme": "zune",
        "placevaluesInside": "1",
        "showCanvasBg": "1",
        "showCanvasBase": "1",
        "canvasBaseDepth": "14",
        "canvasBgDepth": "5",
        "canvasBaseColor": "#aaaaaa",
        "canvasBgColor": "#eeeeee"
    }
    
    date = dt.today()
    categories_list = []
    dataset = [{'seriesname':'Today'}]
    dataset_list = []
    reports = Reports.objects.filter(date=date)
    diseases = []
    for report in reports:
        if report.disease.upper() not in diseases:
            diseases.append(report.disease.upper())
    
    mixed_data = []
    for disease in diseases:
        count = reports.filter(disease__iexact=disease).aggregate(Sum('count'))['count__sum']
        mixed_data.append([count, disease])
    mixed_data.sort()
    mixed_data = mixed_data[-5:]
    mixed_data = mixed_data[::-1]
    
    for data in mixed_data:
        categories_list.append({'label':data[1]})
        dataset_list.append({'value':data[0]})
    dataset[0].update({'data':dataset_list})
    
    dataSource['categories'] = [{
            "category": categories_list
        }]
    
    dataSource['dataset'] = dataset

    
    col2D = FusionCharts("mscolumn3d", "ex1" , "600", "400", "chart-1", "json", dataSource)
    context = {'chart1': col2D.render()}
    html = render(request, 'demo/graph.html', context)
    
    print(html)
    return HttpResponse(html)

def reports(request):
    area = request.GET.get('area')
    Date = dt.today()
    reports = Reports.objects.filter(date=Date).filter(phone_number__code__name_state=area)
    diseases = []
    for report in reports:
        if report.disease.upper() not in diseases:
            diseases.append(report.disease.upper())
            
    phones = Phones.objects.filter(code__name_state=area)
    nums = []
    for phone in phones:
        if phone not in nums:
            nums.append(phone.number)
    total_counts=reports.aggregate(Sum('count'))['count__sum']
    disease_counts = []
    for disease in diseases:
        count = reports.filter(disease__iexact=disease).aggregate(Sum('count'))['count__sum']
        if count:
            disease_counts.append({'name':disease, 'count':count})
    data = {'hosp_code':area,'diseases':disease_counts, 'numbers':nums, 'total_counts':total_counts}
    html = render(request, 'demo/report_listings.html', data)
    return HttpResponse(html)

def states(request):
    data = render(request, 'demo/states_outlines.html')
    return HttpResponse(data, content_type="application/json")

