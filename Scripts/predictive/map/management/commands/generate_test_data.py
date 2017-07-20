from django.core.management.base import BaseCommand
from map.models import LHCP, Phones, Diseases

from datetime import datetime as dt
import random
import csv
import os

class Command(BaseCommand):
    args = '<none>'
    help = 'Generates test data'
    
    def handle(self, *args, **options):
        Phones.objects.all().delete()
        
        phone_list = generate_phone_numbers(500)
        hosp_choices = LHCP.objects.all().count() - 1
        disease_list = Diseases.objects.all().count()
        
        for phone_num in phone_list:
            associate_phone_location(phone_num, hosp_choices)
        
        test_phones = phones_for_data(500)
        
        data = []
        for phone in test_phones:
            disease = get_disease(disease_list)
            report_type = head_count_or_deaths()
            cases = case_count_generator(report_type)
            message_body = report_type + "; " + disease + "; " + str(cases)
            date = dt.today().strftime('%Y-%m-%d')
            data.append([phone.number, message_body, date])
        
        os.chdir(os.getcwd() + '\\testdata')
        date_now = dt.now().strftime('%m%d%Y%I%M%S%f')
        with open('test-data-'+date_now+'.csv', 'w', newline='') as outfile:
            outwriter = csv.writer(outfile, delimiter=',')
            outwriter.writerows(data)         
        
        
#ensures that the necessary number of random phone numbers exists
def generate_phone_numbers(data_point_count):
    list_of_nums = []
    current_count = Phones.objects.all().count()
    count_diff = data_point_count - current_count
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

#associate phone numbers with a local health care provider
def associate_phone_location(phone_num, hosp_choices):
    idx = random.randint(0, hosp_choices)
    Phones.objects.create(
            number = phone_num,
            hospital = LHCP.objects.all()[idx]
        )

#grabs a random disease
def get_disease(diseases_count):
    idx = random.randint(0, diseases_count - 1)
    return Diseases.objects.all()[idx].name

#makes a random choice between head count and death report
def head_count_or_deaths():
    if random.uniform(0,1) < 0.8:
        return "H"
    else:
        return "D"

#generates a random number of cases
def case_count_generator(h_or_d):
    added_randomness = random.uniform(0,1)
    if h_or_d == "H":
        if added_randomness < 0.5:
            count = random.normalvariate(20,3)
        elif added_randomness < 0.75:
            count = random.normalvariate(50,5)
        elif added_randomness > 0.999:
            count = random.normalvariate(1000,50)
        else:
            count = random.normalvariate(100, 10)
    else:
        if added_randomness < 0.7:
            count = random.normalvariate(3,1)
        elif added_randomness < 0.9:
            count = random.normalvariate(7,2)
        elif added_randomness > 0.9999:
            count = random.normalvariate(10000,1000)
        else:
            count = random.normalvariate(100,10)
    return round(count)

#selects a random set of the phones from the models
def phones_for_data(data_point_count):
    phones = Phones.objects.all()
    test_phones = []
    for i in range(data_point_count):
        already_chosen = True
        while already_chosen:
            num = random.randint(0,phones.count() - 1)
            phone_num = phones[num]
            if phone_num not in test_phones:
                test_phones.append(phone_num)
                already_chosen = False
    return test_phones