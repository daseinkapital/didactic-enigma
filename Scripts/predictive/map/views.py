from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, Sum

from .fusioncharts import FusionCharts

import json

from datetime import datetime as dt
from .models import Districts, HeadReports, Diseases


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

def graphs(request):
    dataSource = {}
    
    dataSource["chart"] = {
        "caption": "Ebola by District",
        "subCaption": "Sierra Leone",
        "xAxisName": "District",
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
    
    date = dt.strptime('2017-07-27', '%Y-%m-%d')
    categories_list = []
    dataset = [{'seriesname':'2017-07-27'}]
    dataset_list = []
    districts = Districts.objects.all()
    reports = HeadReports.objects.filter(date=date).filter(disease__name='Ebola')
    for district in districts:
        categories_list.append({'label':district.name})
        data = reports.filter(phone_number__hospital__district=district).aggregate(Sum('count'))['count__sum']
        if data != None:
            dataset_list.append({'value':data})
        else:
            dataset_list.append({'value':0})
    dataset[0].update({'data':dataset_list})
    
    dataSource['categories'] = [{
            "category": categories_list
        }]
    
    dataSource['dataset'] = dataset
    print(dataSource)
    
    col2D = FusionCharts("mscolumn3d", "ex1" , "600", "400", "chart-1", "json", dataSource)
    
        
    zoom_line_chart_details = {
                "caption": "Disease Levels",
                "subcaption": "Last 100 Days",
                "yaxisname": "Case Count",
                "xaxisname": "Date",
                "yaxisminValue": "0",
                "yaxismaxValue": "3000",
                "pixelsPerPoint": "0",
                "pixelsPerLabel": "30",
                "lineThickness": "1",
                "compactdatamode": "1",
                "dataseparator": "|",
                "labelHeight": "30",
                "theme": "fint"
            }
    
    reports = HeadReports.objects.all().order_by('date')
    dates = []
    date_objs = []
    for row in reports:
        if row.date.strftime('%b %d') not in dates:
            dates.append(row.date.strftime('%b %d'))
            date_objs.append(row.date)
    
    
    categories = ""
    for date in dates:
        categories += date + "|"
    categories = categories[:-1]
    
    zoom_line_chart_categories = [
            {
                "category": categories
            }
        ]
    
    datasets = []
    diseases = Diseases.objects.all()
    for disease in diseases:
        data = ""
        for date in date_objs:
            point = reports.filter(disease__name=disease.name).filter(date=date).aggregate(Sum('count'))['count__sum']
            data += str(point) + "|"
        data = data[:-1]
        datasets.append({'seriesname':disease.name, 'data':data})
    
        
    
    zoom_line_chart_input = {'chart' : zoom_line_chart_details, 'categories': zoom_line_chart_categories, 'dataset':datasets}

    print(zoom_line_chart_input)
    
    zoom_line = FusionCharts("zoomline", "ex2" , "600", "400", "chart-2", "json", zoom_line_chart_input)
    return render(request, 'map/graphs.html', {'output_2dcol': col2D.render(), 'output_zoom_line': zoom_line.render()})

def make_dataset_zoom_line(Reports):

    
    pass