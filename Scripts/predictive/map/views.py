from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

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
    report_dates = Reports.objects.order_by('date').distinct('date')
    context = {'report_dates' : report_dates}
    districts = Districts.objects.all()
    context.update({'districts':districts})
    return render(request, 'map/product.html', context)
    
        
