from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.

from .models import Districts

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

def data(request):
    button_name = request.GET.get('direction', None)
    if 'South' in button_name:
        most_south = Districts.objects.order_by('longitude')[:5]
        context = {'most_south':most_south}
        html = render(request, 'map/siderbar.html', context)
        data = { 'html' : html }
        return JsonResponse(data)
    else:
        return JsonResponse({ 'html' : '<h1> Whoops </h1> '})
    
def product(request):
    most_north = Districts.objects.order_by('-longitude')[:5]
    context = {'most_north':most_north}
    most_south = Districts.objects.order_by('longitude')[:5]
    context.update({'most_south':most_south})
    most_west = Districts.objects.order_by('latitude')[:5]
    context.update({'most_west':most_west})
    most_east = Districts.objects.order_by('-latitude')[:5]
    context.update({'most_east':most_east})
    return render(request, 'map/product.html', context)
    
        
