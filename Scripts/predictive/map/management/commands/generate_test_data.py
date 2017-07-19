from django.core.management.base import BaseCommand
from map.models import LHCP, Districts, Reports, Phones

import random
import csv

class Command(BaseCommand):
    args = '<none>'
    help = 'Generates test data'
    
    def handle(self, *args, **options):
        phone_list = generate_phone_numbers(500)
        hosp_choices = LHCP.objects.all().count() - 1
        phone_objs = Phones.objects.all()
        for phone_num in phone_list:
            associate_phone_location(phone_num, hosp_choices)
        
                
                


def generate_phone_numbers(count):
    list_of_nums = []
    current_count = Phones.objects.all().count()
    count_diff = current_count - count
    if count_diff > 0:
        for i in range(count_diff):
            number = str(random.randint(0000000, 9999999))
            padding = 7 - len(number)
            number = "0"*padding + number
            if number in list_of_nums:
                if Phones.objects.filter(number=number).first():
                    list_of_nums = generate_phone_numbers(list_of_nums)
            else:
                list_of_nums.append(number)
    return list_of_nums

def associate_phone_location(phone_num, hosp_choices):
    idx = random.randint(0, hosp_choices)
    Phones.objects.create(
            number = phone_num,
            hospital = LHCP.objects.all()[idx]
        )

        