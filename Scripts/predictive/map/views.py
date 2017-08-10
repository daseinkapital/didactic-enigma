from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, Sum
from .fusioncharts import FusionCharts
import json

from datetime import datetime as dt
from .models import Districts, HeadReports, DeathReports, Diseases, Phones

def about(request): 
    return render(request,'map/about.html')
def service(request):
    return render(request, 'map/service.html')
def contact(request):
    return render(request, 'map/contact.html')
def blog(request):
    return render(request, 'map/blog.html')
def index(request):
    return render(request, 'map/index.html')

def reports(request):
    districtName, date_string = request.GET.get('name'), request.GET.get('date')
    if districtName == None and date_string == None:
        return render(request, 'map/preselect_reports.html')
    district = Districts.objects.filter(name=districtName)
    context = {'district':districtName}
    Date = dt.strptime(date_string, '%Y-%m-%d')
    headReports = HeadReports.objects.filter(date=Date).filter(phone_number__hospital__district=district).aggregate(Sum('count'))
    context.update({'reports': headReports['count__sum']})
    html = render(request, 'map/reports.html', context)
    return HttpResponse(html)
    
def downloads(request):
    return render(request, 'map/downloads.html')

##populates sidebar upon clicking a district highlighted 
def marker(request):
    districtName, date_string = request.GET.get('name'),request.GET.get('date')
    district = Districts.objects.filter(name=districtName)
    context = {'district':districtName}
    Date = dt.strptime(date_string, '%Y-%m-%d')
    headReports = HeadReports.objects.filter(date=Date).filter(phone_number__hospital__district=district).aggregate(Sum('count'))
    context.update({'reports': headReports['count__sum']})
    html = render(request, 'map/sidebar_data.html', context)
    return HttpResponse(html)

##sneding json data back to ol-district-map.js to populate the points for reports
def addcases(request):
    districtName = request.GET.get('name')
    print(request.GET.get)
    reportsdict ={}
    district = Districts.objects.filter(name=districtName).first()
    i = 0
    Date = dt.strptime("2017-07-27","%Y-%m-%d")
    reports = HeadReports.objects.filter(date=Date).filter(phone_number__hospital__district=district)
    hospitals = []
    for report in reports:
        if report.phone_number.hospital.name not in hospitals:
            hospitals.append(report.phone_number.hospital.name)
    
    data = []
    for hospital in hospitals:
        report = reports.filter(phone_number__hospital__name=hospital)
        hospitalName = hospital
        lat = report.first().phone_number.hospital.lat
        lng = report.first().phone_number.hospital.lng
        case_count = report.aggregate(Sum('count'))['count__sum']
        data.append([hospitalName, lat, lng, case_count])
    
    data.sort(key=lambda x: x[3])
    j = len(data)
    for row in data:
        reportsdict.update({i : {'hospitalName': row[0], 'lat' : str(row[1]), 'lng' : str(row[2]), 'deaths' : str(row[3]), 'zval': str(j)}})
        i += 1
        j -= 1
    
    data = json.dumps(reportsdict)
    return HttpResponse(data, content_type="application/json")
    
def product(request):
    if request.GET.get('visit') == "first":
        return render(request, 'map/product_first_visit.html')
    else:
        return render(request, 'map/product.html')

##loads the main map from ajax call
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

def pop_region(request):
    districtName = request.GET.get('name')
    district = Districts.objects.filter(name=districtName).first()
    districtdict = {}
    i = 0
    Date = dt.strptime("2014-09-18","%Y-%m-%d")
    size_scale = [10, 100, 1000, 10000]
    reports = HeadReports.objects.filter(date=Date).filter(phone_number__hospital__district=district)
    for report in reports:    
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
    map_data = {'zoom' : str(districts.zoom), 'lat' : str(districts.lat), 'lng' : str(districts.lng)}
    data = json.dumps(map_data)
    return HttpResponse(data, content_type="application/json")

def districts(request):
    data = render(request, 'map/jsonResponse.html')
    return HttpResponse(data, content_type="application/json")

def indDistricts(request):
    data = render(request, 'map/districtJson.html')
    return HttpResponse(data, content_type="application/json")

def region(request, district):
    dist_obj = Districts.objects.filter(name__iexact=district).first()
    context = {'district_name' : district, 'dist': dist_obj}
    return render(request, 'map/region.html', context)

@csrf_exempt
def sms(request):
    message = request.POST.get('Body')
    from_number = request.POST.get('From')
    print(message)
    print(from_number)
    return HttpResponse('<h1>Nice</h1>')

##sending json data to ajax for react calendar    
def changedate(request):
    startDate = dt.strptime(request.GET.get('startdate'), '%Y-%m-%d'), dt.strptime(request.GET.get('enddate'), '%Y-%m-%d')
    districts = Districts.objects.all()
    districtdict = {} 
    i = 0
    size_scale = [10, 100, 1000, 10000]
    for district in districts:
        report = HeadReports.objects.filter(date__gte=startDate).filter(phone_number__hospital__district=district)
        if report:
            s = 1
            for size in size_scale:
                if report.count > size:
                    s += 1
                else:
                    break
            corddict = {i : {'name': district.name, 'lat' : str(district.latitude), 'lng' : str(district.longitude), 'deaths' : str(report.count), 'size' : s}}
            districtdict.update(corddict)
            i += 1
    data = json.dumps(districtdict)
    return HttpResponse(data, content_type="application/json")

def hosp_overview(request):
    hosp_code = request.GET.get('code')
    reports = HeadReports.objects.filter(phone_number__hospital__name=hosp_code).filter(date='2017-07-27')
    diseases = Diseases.objects.all()
    phones = Phones.objects.filter(hospital__name=hosp_code)
    nums = []
    for phone in phones:
        nums.append(phone.number)
    total_counts=reports.aggregate(Sum('count'))['count__sum']
    disease_counts = []
    for disease in diseases:
        count = reports.filter(disease__name=disease.name).aggregate(Sum('count'))['count__sum']
        if count:
            disease_counts.append({'name':disease.name, 'count':count})
    data = {'hosp_code':hosp_code,'diseases':disease_counts, 'numbers':nums, 'total_counts':total_counts}
    return HttpResponse(render(request, 'map/report_listings.html', data))
    
def dist_charts(request):
    district = request.GET.get('name')
    dist_obj = Districts.objects.filter(name__iexact=district).first()
    
    dataSource = {}
    
    dataSource["chart"] = {
        "caption": "Disease Breakdown",
        "subCaption": district,
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
    
    date = dt.strptime('2017-07-27', '%Y-%m-%d')
    categories_list = []
    dataset = [{'seriesname':'2017-07-27'}]
    dataset_list = []
    diseases = Diseases.objects.all()
    reports = HeadReports.objects.filter(date=date).filter(phone_number__hospital__district=dist_obj)
    for disease in diseases:
        categories_list.append({'label':disease.name})
        data = reports.filter(disease=disease).aggregate(Sum('count'))['count__sum']
        if data != None:
            dataset_list.append({'value':data})
        else:
            dataset_list.append({'value':0})
    dataset[0].update({'data':dataset_list})
    
    dataSource['categories'] = [{
            "category": categories_list
        }]
    
    dataSource['dataset'] = dataset

    
    col3D = FusionCharts("mscolumn3d", "ex1" , "400", "300", "chart-1", "json", dataSource)
    
        
    zoom_line_chart_details = {
                "caption": "Daily Reports",
                "subcaption": "Last 100 Days",
                "yaxisname": "Number of Reports Submitted",
                "xaxisname": "Date",
                "yaxisminValue": "0",
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
    data = ""
    for date in date_objs:
        point = reports.filter(phone_number__hospital__district=dist_obj).filter(date=date).count()
        data += str(point) + "|"
    data = data[:-1]
    datasets.append({'seriesname':'Disease Report Counts', 'data':data})
    
        
    
    zoom_line_chart_input = {'chart' : zoom_line_chart_details, 'categories': zoom_line_chart_categories, 'dataset':datasets}
    
    zoom_line1 = FusionCharts("zoomline", "ex2" , "400", "300", "chart-2", "json", zoom_line_chart_input)
    
    
    #Second zoom line chart
    zoom_line_chart_details = {
            "caption": "Disease Levels",
            "subcaption": "Last 100 Days",
            "yaxisname": "Case Count",
            "xaxisname": "Date",
            "yaxisminValue": "0",
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
            point = reports.filter(disease__name=disease.name).filter(date=date).filter(phone_number__hospital__district=dist_obj).aggregate(Sum('count'))['count__sum']
            data += str(point) + "|"
        data = data[:-1]
        datasets.append({'seriesname':disease.name, 'data':data})
    
        
    
    zoom_line_chart_input = {'chart' : zoom_line_chart_details, 'categories': zoom_line_chart_categories, 'dataset':datasets}
    zoom_line2 = FusionCharts("zoomline", "ex3" , "400", "300", "chart-3", "json", zoom_line_chart_input)
    
    context = {'chart1': col3D.render(), 'chart2': zoom_line1.render(), 'chart3': zoom_line2.render()}        
    html = render(request, 'map/region-charts.html', context)
    return HttpResponse(html)

def country_charts(request):
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

    
    col2D = FusionCharts("mscolumn3d", "ex1" , "400", "300", "chart-1", "json", dataSource)
    
        
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
            if point != None:
                data += str(point) + "|"
            else:
                data += "0|"
        data = data[:-1]
        datasets.append({'seriesname':disease.name, 'data':data})
    
        
    
    zoom_line_chart_input = {'chart' : zoom_line_chart_details, 'categories': zoom_line_chart_categories, 'dataset':datasets}

    
    zoom_line = FusionCharts("zoomline", "ex2" , "400", "300", "chart-2", "json", zoom_line_chart_input)
    context = {'chart1': col2D.render(), 'chart2': zoom_line.render()}
    
    html = render(request, 'map/graph_country_view.html', context)
    return HttpResponse(html)
    