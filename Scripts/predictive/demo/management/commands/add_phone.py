from django.core.management.base import BaseCommand
from demo.models import Phones, Reports, Cities

import random

class Command(BaseCommand):
    args = '<none really>'
    help = 'Adds phone number to database when someone texts in'
    
    #allow the user to specify switches for the mgmt command
    def add_arguments(self, parser):
        parser.add_argument(
                'disease',
                nargs=1,
                type=str
            )
        
        parser.add_argument(
                'count',
                nargs=1,
                type=int
            )
        
        parser.add_argument(
                'phone',
                nargs=1,
                type=str
            )
    
    #main function control
    def handle(self, *args, **options):
        disease = options['disease'][0].upper()
        cases = options['count'][0]
        phone_num = options['phone'][0]
        
#        print(disease)
#        print(cases)
#        print(phone_num)
#        exit()
        
        phone_exists = Phones.objects.filter(number=phone_num).first()
        
        if not phone_exists:
        
            area_code = phone_num[2:5]
            
            city_count = Cities.objects.filter(code=area_code).count()
            if city_count == 0:
                city_choices = Cities.objects.all()
            else:
                city_choices = Cities.objects.filter(code=area_code)
 
            city = random.choice(city_choices)
            
            Phones.objects.create(
                    number=phone_num,
                    code=city
                )
        
        phone = Phones.objects.filter(number=phone_num).first()
        
        Reports.objects.create(
                    count=cases,
                    disease=disease,
                    phone_number=phone
                )