from django.core.management.base import BaseCommand
from django.core import management #use management.call_command
from map.models import LHCP, Phones, Diseases, AltDiseases
from map.management.commands.generate_test_data import (generate_phone_numbers,
                                                        associate_phone_location,
                                                        get_disease,
                                                        head_count_or_deaths,
                                                        case_count_generator,
                                                        phones_for_data)

import os
import csv
import random
import math
from datetime import datetime as dt
from datetime import timedelta as td


class Command(BaseCommand):
    args = '<none really>'
    help = 'Generates test data for fringe cases of outbreaks'
    
    #This is a global format for date parsing. If the date ever changes, change it here and it will
    #be reflected all through out the document
    date_format = '%Y-%m-%d'
    
    #allow the user to specify switches for the mgmt command
    def add_arguments(self, parser):
        parser.add_argument(
                '--disease',
                action = 'store_true',
                dest = 'disease',
                default = False,
                help = 'Create data that shows a spread of a specified disease. Three months worth of data will be created.'
            )
        
        parser.add_argument(
                '--epicenter',
                action = 'store_true',
                dest = 'epicenter',
                default = False,
                help = 'Choose a given coordinate set where a disease spike spreads from (longitude, latitude)'
            )
        
        parser.add_argument(
                '--rapid',
                action = 'store_true',
                dest = 'rapid',
                default = False,
                help = 'Create data for a quick spread scenario'
            )
        
        parser.add_argument(
                '--slow',
                action = 'store_true',
                dest = 'slow',
                default = False,
                help = 'Create data from a slower spread scenario'
            )
        
        parser.add_argument(
                '--days',
                nargs = 1,
                type = int,
                default = [90],
                help = 'Specify the number of days to make test data with (defaults to 90)'
            )
        
        parser.add_argument(
                '--reports',
                nargs = 2,
                type = int,
                default = [100,300],
                help = 'Specify the upper and lower bounds of the number of reports made on each day'
            )
        
        parser.add_argument(
                '--epi-spec',
                nargs = 2,
                type = float,
                help = 'Specify the epicenter longitude/latitude of a disease outbreak (only affects when epicenter is chosen)'
            )
        
        parser.add_argument(
                '--disease-spec',
                nargs = 1,
                type = str,
                help = 'Specify the disease to have an outbreak of (only affects when the disease switch is present)'
            )
        
        parser.add_argument(
                '--epi-increment',
                nargs = 1,
                type = float,
                default = [0.005],
                help = 'Specify the increment step of an epicenter disease outbreak (default is 0.005 lat/lng)'
            )
        
        parser.add_argument(
                '--epi-radius',
                nargs = 1,
                type = float,
                default = [0.05],
                help = 'Specify the initial radius of an epicenter-based disease outbreak (default is 0.05 lat/lng)'
            )
        
        parser.add_argument(
                '--all',
                action='store_true',
                dest='all',
                default=False,
                help= 'Set the disease, epicenter and slow switch all on'
            )
    
    #main function control
    def handle(self, *args, **options):
            #set the working directory to save in the testdata folder
            os.chdir(os.getcwd() + '\\testdata')
            
            if options['all']:
                options['disease'] = True
                options['epicenter'] = True
                options['slow'] = True
            
            end_date = dt.today()
            start_date = end_date - td(days=options['days'][0])
            num_days = end_date - start_date
            num_days = num_days.days + 1
            random_num_list = list(range(options['days'][0]))
            lower, upper = min(options['reports']), max(options['reports'])
            
            add_options = options
            add_options.update({
                    'start':start_date,
                    'num_days':num_days,
                    'random_list':random_num_list,
                    'lower':lower,
                    'upper':upper
                })
            
            #if an epicenter is specified, assign it in the options
            if options['epi_spec']:
                epi_lng = options['epi_spec'][0]
                epi_lat = options['epi_spec'][1]
                add_options.update({
                        'lat':epi_lat,
                        'lng':epi_lng
                    })
                options['epicenter'] = True
            
            #if a disease is specified, assign its official name to the additional options
            if options['disease_spec']:
                if AltDiseases.objects.filter(alt_name__iexact=options['disease_spec'][0]).first():
                    disease = AltDiseases.objects.filter(alt_name__iexact=options['disease_spec'][0]).first().official_name.name
                    add_options.update({
                            'disease_name':disease
                        })
                options['disease'] = True
    
            if options['disease']:
                if options['epicenter']:
                    if options['rapid'] or options['slow']:
                        create_disease_outbreak_epicenter_timeframe(add_options)
                        print('Done.')
                    else:
                        create_disease_outbreak_epicenter(add_options)
                        print('Done.')
                elif options['rapid'] or options['slow']:
                    create_disease_outbreak_timeframe(add_options)
                    print('Done.')
                else:
                    create_disease_outbreak(add_options)
                    print('Done.')
            
            elif options['epicenter']:
                if options['rapid'] or options['slow']:
                    create_disease_epicenter_timeframe(add_options)
                    print('Done.')
                else:
                    create_disease_epicenter(add_options)
                    print('Done.')
                    
            elif options['rapid'] or options['slow']:
                create_disease_timeframe(add_options)
                print('Done.')
            
            else:
                create_disease(add_options)
                print('Done.')

#generically creates data. Essentially only calls the
#generate_test_data command, so it is recommended that this
#not be used.                            
def create_disease(add_options):
    for day in range(add_options['num_days']):
        
        date = increment_date(add_options, day)
        
        management.call_command(
                            'generate_test_data',
                            random_data=add_options['reports'],
                            date=[date],
                            no_dir_change=True,
                            test_supress=True
                        )
#creates an increase for a specific disease, from a specific
#starting point, at a specific rate
def create_disease_outbreak_epicenter_timeframe(add_options):
    #initialize timeframe related variables
    if add_options['rapid']:
        mean_shift_base = 3
        mean_shift_factor = 1.2
    elif add_options['slow']:
        mean_shift_base = 1
        mean_shift_factor = 1.05
    shift = mean_shift_base
    
    #initialize epicenter related variables
    if 'lng' in add_options:
        epicenter = {'lng' : add_options['lng'], 'lat' : add_options['lat']}
    else:
        random_lat = random.uniform(7,10)
        random_lng = random.uniform(-10.5, -13)
        epicenter = {'lng' : random_lng, 'lat' : random_lat}
    spread_radius = add_options['epi_radius'][0]
    spread_increment = add_options['epi_increment'][0]
    
    #initialize outbreak related variables
    if 'disease_name' in add_options:
        outbreak_disease = add_options['disease_name']
    else:
        disease_count = Diseases.objects.all().count()
        outbreak_disease = get_disease(disease_count)
    
    #initialize general randomization variables
    outbreak = False
    random_num_list = add_options['random_list']
    
    for day in range(add_options['num_days']):
        
        date = increment_date(add_options, day)
        
        if not outbreak:
            random_num = random.choice(random_num_list)
            random_num_list.remove(random_num)
            if (random_num*5) < day:
                outbreak = True
                if add_options['rapid']:
                    print("A rapid outbreak of " + outbreak_disease + " has begun at "+str(epicenter['lng'])+", "+str(epicenter['lat'])+".")
                elif add_options['slow']:
                    print("A slow outbreak of " + outbreak_disease + " has begun at "+str(epicenter['lng'])+", "+str(epicenter['lat'])+".")
        if outbreak:
            #increment the amount of spread
            spread_radius += spread_increment
            #set bounds for spread
            upper_lat = epicenter['lat'] + spread_radius
            upper_lng = epicenter['lng'] + spread_radius
            lower_lat = epicenter['lat'] - spread_radius
            lower_lng = epicenter['lng'] - spread_radius
            #query phones "consumed" by spread
            phones_in_outbreak = Phones.objects.filter(hospital__lat__gte=lower_lat)
            phones_in_outbreak = phones_in_outbreak.filter(hospital__lat__lte=upper_lat)
            phones_in_outbreak = phones_in_outbreak.filter(hospital__lng__gte=lower_lng)
            phones_in_outbreak = phones_in_outbreak.filter(hospital__lng__lte=upper_lng)
            #set shift
            shift = shift*mean_shift_factor
            count = random.randint(add_options['lower'],add_options['upper'])
            write_test_data_outbreak_epicenter_timeframe(count, date, shift, phones_in_outbreak, outbreak_disease)
            print("Data created for "+ date)
        
        #if no outbreak has occured yet, create a regular number of reports
        else:
            management.call_command(
                    'generate_test_data',
                    random_data=add_options['reports'],
                    date=[date],
                    no_dir_change=True,
                    test_supress=True
                )
            

def create_disease_outbreak_epicenter(add_options):
    #initialize epicenter related variables
    if 'lng' in add_options:
        epicenter = {'lng' : add_options['lng'], 'lat' : add_options['lat']}
    else:
        random_lat = random.uniform(7,10)
        random_lng = random.uniform(-10.5, -13)
        epicenter = {'lng' : random_lng, 'lat' : random_lat}
    spread_radius = add_options['epi_radius'][0]
    spread_increment = add_options['epi_increment'][0]
    
    #initialize outbreak related variables
    if 'disease_name' in add_options:
        outbreak_disease = add_options['disease_name']
    else:
        disease_count = Diseases.objects.all().count()
        outbreak_disease = get_disease(disease_count)
    
    #initialize general randomization variables
    outbreak = False
    random_num_list = add_options['random_list']
    
    for day in range(add_options['num_days']):
        
        date = increment_date(add_options, day)
        
        if not outbreak:
            random_num = random.choice(random_num_list)
            random_num_list.remove(random_num)
            if (random_num*5) < day:
                outbreak = True
                print("An outbreak of " + outbreak_disease + " has begun at "+str(epicenter['lng'])+", "+str(epicenter['lat'])+".")

        if outbreak:
            #increment the amount of spread
            spread_radius += spread_increment
            #set bounds for spread
            upper_lat = epicenter['lat'] + spread_radius
            upper_lng = epicenter['lng'] + spread_radius
            lower_lat = epicenter['lat'] - spread_radius
            lower_lng = epicenter['lng'] - spread_radius
            #query phones "consumed" by spread
            phones_in_outbreak = Phones.objects.filter(hospital__lat__gte=lower_lat)
            phones_in_outbreak = phones_in_outbreak.filter(hospital__lat__lte=upper_lat)
            phones_in_outbreak = phones_in_outbreak.filter(hospital__lng__gte=lower_lng)
            phones_in_outbreak = phones_in_outbreak.filter(hospital__lng__lte=upper_lng)
            #randomize the count
            count = random.randint(add_options['lower'],add_options['upper'])
            write_test_data_outbreak_epicenter(count, date, phones_in_outbreak, outbreak_disease)
            print("Data created for "+ date)
        
        #if no outbreak has occured yet, create a regular number of reports
        else:
            management.call_command(
                    'generate_test_data',
                    random_data=add_options['reports'],
                    date=[date],
                    no_dir_change=True,
                    test_supress=True
                )


def create_disease_outbreak_timeframe(add_options):
    #initialize timeframe related variables
    if add_options['rapid']:
        mean_shift_base = 3
        mean_shift_factor = 1.2
    elif add_options['slow']:
        mean_shift_base = 1
        mean_shift_factor = 1.05
    shift = mean_shift_base
    
    #initialize outbreak related variables

    if 'disease_name' in add_options:
        outbreak_disease = add_options['disease_name']
    else:
        disease_count = Diseases.objects.all().count()
        outbreak_disease = get_disease(disease_count)
    
    #initialize general randomization variables
    outbreak = False
    random_num_list = add_options['random_list']
    
    for day in range(add_options['num_days']):
        
        date = increment_date(add_options, day)
        
        if not outbreak:
            random_num = random.choice(random_num_list)
            random_num_list.remove(random_num)
            if (random_num*5) < day:
                outbreak = True
                if add_options['rapid']:
                    print("A rapid outbreak of " + outbreak_disease + " has begun.")
                elif add_options['slow']:
                    print("A slow outbreak of " + outbreak_disease + " has begun.")
        if outbreak:
            #set shift
            shift = shift*mean_shift_factor
            count = random.randint(add_options['lower'],add_options['upper'])
            write_test_data_outbreak_timeframe(count, date, shift, outbreak_disease)
            print("Data created for "+ date)
        
        #if no outbreak has occured yet, create a regular number of reports
        else:
            management.call_command(
                    'generate_test_data',
                    random_data=add_options['reports'],
                    date=[date],
                    no_dir_change=True,
                    test_supress=True
                )


def create_disease_epicenter_timeframe(add_options):
        #initialize timeframe related variables
    if add_options['rapid']:
        mean_shift_base = 3
        mean_shift_factor = 1.2
    elif add_options['slow']:
        mean_shift_base = 1
        mean_shift_factor = 1.05
    shift = mean_shift_base
    
    #initialize epicenter related variables
    if 'lng' in add_options:
        epicenter = {'lng' : add_options['lng'], 'lat' : add_options['lat']}
    else:
        random_lat = random.uniform(7,10)
        random_lng = random.uniform(-10.5, -13)
        epicenter = {'lng' : random_lng, 'lat' : random_lat}
    spread_radius = add_options['epi_radius'][0]
    spread_increment = add_options['epi_increment'][0]
    
    
    #initialize general randomization variables
    outbreak = False
    random_num_list = add_options['random_list']
    
    for day in range(add_options['num_days']):
        
        date = increment_date(add_options, day)
        
        if not outbreak:
            random_num = random.choice(random_num_list)
            random_num_list.remove(random_num)
            if (random_num*5) < day:
                outbreak = True
                if add_options['rapid']:
                    print("A rapid outbreak has begun at "+str(epicenter['lng'])+", "+str(epicenter['lat'])+".")
                elif add_options['slow']:
                    print("A slow outbreak has begun at "+str(epicenter['lng'])+", "+str(epicenter['lat'])+".")
        if outbreak:
            #increment the amount of spread
            spread_radius += spread_increment
            #set bounds for spread
            upper_lat = epicenter['lat'] + spread_radius
            upper_lng = epicenter['lng'] + spread_radius
            lower_lat = epicenter['lat'] - spread_radius
            lower_lng = epicenter['lng'] - spread_radius
            #query phones "consumed" by spread
            phones_in_outbreak = Phones.objects.filter(hospital__lat__gte=lower_lat)
            phones_in_outbreak = phones_in_outbreak.filter(hospital__lat__lte=upper_lat)
            phones_in_outbreak = phones_in_outbreak.filter(hospital__lng__gte=lower_lng)
            phones_in_outbreak = phones_in_outbreak.filter(hospital__lng__lte=upper_lng)
            #set shift
            shift = shift*mean_shift_factor
            count = random.randint(add_options['lower'],add_options['upper'])
            write_test_data_epicenter_timeframe(count, date, shift, phones_in_outbreak)
            print("Data created for "+ date)
        
        #if no outbreak has occured yet, create a regular number of reports
        else:
            management.call_command(
                    'generate_test_data',
                    random_data=add_options['reports'],
                    date=[date],
                    no_dir_change=True,
                    test_supress=True
                )


#creates an increase for disease at a certain rate                
def create_disease_timeframe(add_options):
    if add_options['rapid']:
        mean_shift_base = 3
        mean_shift_factor = 1.2
    elif add_options['slow']:
        mean_shift_base = 1
        mean_shift_factor = 1.05
    shift = mean_shift_base
    outbreak = False
    random_num_list = add_options['random_list']
    
    for day in range(add_options['num_days']):
        
        date = increment_date(add_options, day)
        
        if not outbreak:
            random_num = random.choice(random_num_list)
            random_num_list.remove(random_num)
            if (random_num*5) < day:
                outbreak = True
                if add_options['rapid']:
                    print("Rapid case reporting initiated.")
                elif add_options['slow']:
                    print("Slow case reporting initiated.")
        
        if outbreak:
            shift = shift*mean_shift_factor
            count = random.randint(add_options['lower'],add_options['upper'])
            write_test_data_timeframe(count, date, shift)
            print("Data created for "+ date)
            
                
        #if no outbreak has occured yet, create a regular number of reports
        else:
            management.call_command(
                    'generate_test_data',
                    random_data=add_options['reports'],
                    date=[date],
                    no_dir_change=True,
                    test_supress=True
                )
                
                
                
#generates a disease outbreak based on an epicenter that slowly grows larger
#and larger. Local health care providers affected by the epicenter will notice
#an overall uptick in all disease
def create_disease_epicenter(add_options):
    if 'lng' in add_options:
        epicenter = {'lng' : add_options['lng'], 'lat' : add_options['lat']}
    else:
        random_lat = random.uniform(7,10)
        random_lng = random.uniform(-10.5, -13)
        epicenter = {'lng' : random_lng, 'lat' : random_lat}
    spread_radius = add_options['epi_radius'][0]
    spread_increment = add_options['epi_increment'][0]
    outbreak = False
    random_num_list = add_options['random_list']
    
    for day in range(add_options['num_days']):
        
        date = increment_date(add_options, day)
        
        #if an outbreak has yet to occur, roll to see if it will happen
        if not outbreak:
            random_num = random.choice(random_num_list)
            random_num_list.remove(random_num)
            if (random_num*5) < day:
                outbreak = True
                print("A disease spread has emerged from "+str(epicenter['lng'])+", "+str(epicenter['lat'])+".")
        #check to see if we triggered an outbreak
        if outbreak:
            #increment the amount of spread
            spread_radius += spread_increment
            #set bounds for spread
            upper_lat = epicenter['lat'] + spread_radius
            upper_lng = epicenter['lng'] + spread_radius
            lower_lat = epicenter['lat'] - spread_radius
            lower_lng = epicenter['lng'] - spread_radius
            #query phones "consumed" by spread
            phones_in_outbreak = Phones.objects.filter(hospital__lat__gte=lower_lat)
            phones_in_outbreak = phones_in_outbreak.filter(hospital__lat__lte=upper_lat)
            phones_in_outbreak = phones_in_outbreak.filter(hospital__lng__gte=lower_lng)
            phones_in_outbreak = phones_in_outbreak.filter(hospital__lng__lte=upper_lng)
            
            #run write_data given there is an epicenter outbreak
            count = random.randint(add_options['lower'],add_options['upper'])
            write_test_data_epicenter(count, date, phones_in_outbreak)
            print("Data created for "+ date)
            
                
        #if no outbreak has occured yet, create a regular number of reports
        else:
            management.call_command(
                    'generate_test_data',
                    random_data=add_options['reports'],
                    date=[date],
                    no_dir_change=True,
                    test_supress=True
                )

#creates a simulated disease outbreak by choosing a disease and increasing the
#probability of a report of the chosen disease              
def create_disease_outbreak(add_options):
    disease_count = Diseases.objects.all().count()
    if 'disease_name' in add_options:
        outbreak_disease = add_options['disease_name']
    else:
        outbreak_disease = get_disease(disease_count)
    outbreak = False
    random_num_list = add_options['random_list']

    for day in range(add_options['num_days']):
        
        date = increment_date(add_options, day)

        if not outbreak:
            random_num = random.choice(random_num_list)
            random_num_list.remove(random_num)
            if (random_num*5) < day:
                outbreak = True
                print("An outbreak of "+outbreak_disease+" has occured.")
        if outbreak:
            count = random.randint(add_options['lower'],add_options['upper'])
            write_test_data_disease(count, date, outbreak_disease)
            print("Data created for "+ date)
        else:
            management.call_command(
                    'generate_test_data',
                    random_data=add_options['reports'],
                    date=[date],
                    no_dir_change=True,
                    test_supress=True
                )                

#Writes test data based on a specific disease outbreaking from an epicenter at a given rate
def write_test_data_outbreak_epicenter_timeframe(count, data_date, shift, outbreak_phones, disease_name):
    phone_list = generate_phone_numbers(count)
    hosp_choices = LHCP.objects.all().count() - 1
    disease_list = Diseases.objects.all().count()
    
    for phone_num in phone_list:
        associate_phone_location(phone_num, hosp_choices)
    
    test_phones = phones_for_data(count)
    
    data = []
    for phone in outbreak_phones:
        disease = get_outbreak_disease(disease_list, disease_name)
        if phone.number in test_phones:
            test_phones.remove(phone.number)
        report_type = head_count_or_deaths()
        cases = case_count_mean_shift_generator(report_type, shift)
        message_body = report_type + "; " + disease + "; " + str(cases)
        data.append([phone.number, message_body, data_date])
        
    for phone in test_phones:
        disease = get_disease(disease_list)
        report_type = head_count_or_deaths()
        cases = case_count_generator(report_type)
        message_body = report_type + "; " + disease + "; " + str(cases)
        data.append([phone.number, message_body, data_date])
    
    date_now = dt.now().strftime('%m%d%Y%I%M%S%f')
    with open('test-data-'+date_now+'.csv', 'w', newline='') as outfile:
        outwriter = csv.writer(outfile, delimiter=',')
        outwriter.writerows(data)

#Writes test data based on a specific disease outbreaking from an epicenter at a given rate
def write_test_data_outbreak_timeframe(count, data_date, shift, disease_name):
    phone_list = generate_phone_numbers(count)
    hosp_choices = LHCP.objects.all().count() - 1
    disease_list = Diseases.objects.all().count()
    
    for phone_num in phone_list:
        associate_phone_location(phone_num, hosp_choices)
    
    test_phones = phones_for_data(count)
    
    data = []
    for phone in test_phones:
        disease = get_outbreak_disease(disease_list, disease_name)
        report_type = head_count_or_deaths()
        cases = case_count_mean_shift_generator(report_type, shift)
        message_body = report_type + "; " + disease + "; " + str(cases)
        data.append([phone.number, message_body, data_date])
    
    date_now = dt.now().strftime('%m%d%Y%I%M%S%f')
    with open('test-data-'+date_now+'.csv', 'w', newline='') as outfile:
        outwriter = csv.writer(outfile, delimiter=',')
        outwriter.writerows(data)

#Writes test data based on a specific disease outbreaking from an epicenter at a given rate
def write_test_data_outbreak_epicenter(count, data_date, outbreak_phones, disease_name):
    phone_list = generate_phone_numbers(count)
    hosp_choices = LHCP.objects.all().count() - 1
    disease_list = Diseases.objects.all().count()
    
    for phone_num in phone_list:
        associate_phone_location(phone_num, hosp_choices)
    
    test_phones = phones_for_data(count)
    
    data = []
    for phone in outbreak_phones:
        disease = get_outbreak_disease(disease_list, disease_name)
        if phone.number in test_phones:
            test_phones.remove(phone.number)
        report_type = head_count_or_deaths()
        cases = case_count_percent_change_generator(report_type, 1.5)
        message_body = report_type + "; " + disease + "; " + str(cases)
        data.append([phone.number, message_body, data_date])
        
    for phone in test_phones:
        disease = get_disease(disease_list)
        report_type = head_count_or_deaths()
        cases = case_count_generator(report_type)
        message_body = report_type + "; " + disease + "; " + str(cases)
        data.append([phone.number, message_body, data_date])
    
    date_now = dt.now().strftime('%m%d%Y%I%M%S%f')
    with open('test-data-'+date_now+'.csv', 'w', newline='') as outfile:
        outwriter = csv.writer(outfile, delimiter=',')
        outwriter.writerows(data)

#Writes test data based on a specific disease outbreaking from an epicenter at a given rate
def write_test_data_epicenter_timeframe(count, data_date, shift, outbreak_phones):
    phone_list = generate_phone_numbers(count)
    hosp_choices = LHCP.objects.all().count() - 1
    disease_list = Diseases.objects.all().count()
    
    for phone_num in phone_list:
        associate_phone_location(phone_num, hosp_choices)
    
    test_phones = phones_for_data(count)
    
    data = []
    for phone in outbreak_phones:
        disease = get_disease(disease_list)
        if phone.number in test_phones:
            test_phones.remove(phone.number)
        report_type = head_count_or_deaths()
        cases = case_count_mean_shift_generator(report_type, shift)
        message_body = report_type + "; " + disease + "; " + str(cases)
        data.append([phone.number, message_body, data_date])
        
    for phone in test_phones:
        disease = get_disease(disease_list)
        report_type = head_count_or_deaths()
        cases = case_count_generator(report_type)
        message_body = report_type + "; " + disease + "; " + str(cases)
        data.append([phone.number, message_body, data_date])
    
    date_now = dt.now().strftime('%m%d%Y%I%M%S%f')
    with open('test-data-'+date_now+'.csv', 'w', newline='') as outfile:
        outwriter = csv.writer(outfile, delimiter=',')
        outwriter.writerows(data)
            
#Utilize a general mean shift to constantly increase the number of cases reported
def write_test_data_timeframe(count, data_date, shift):
    phone_list = generate_phone_numbers(count)
    hosp_choices = LHCP.objects.all().count() - 1
    disease_list = Diseases.objects.all().count()
    
    for phone_num in phone_list:
        associate_phone_location(phone_num, hosp_choices)
    
    test_phones = phones_for_data(count)
    
    data = []
    for phone in test_phones:
        disease = get_disease(disease_list)
        report_type = head_count_or_deaths()
        cases = case_count_mean_shift_generator(report_type, shift)
        message_body = report_type + "; " + disease + "; " + str(cases)
        data.append([phone.number, message_body, data_date])
    
    date_now = dt.now().strftime('%m%d%Y%I%M%S%f')
    with open('test-data-'+date_now+'.csv', 'w', newline='') as outfile:
        outwriter = csv.writer(outfile, delimiter=',')
        outwriter.writerows(data) 


#save the test data to a file. Utilizes a list of phone numbers near a given
#epicenter to increase the case count
def write_test_data_epicenter(count, data_date, outbreak_phones):
    phone_list = generate_phone_numbers(count)
    hosp_choices = LHCP.objects.all().count() - 1
    disease_list = Diseases.objects.all().count()
    
    for phone_num in phone_list:
        associate_phone_location(phone_num, hosp_choices)
    
    test_phones = phones_for_data(count)
    
    data = []
    for phone in outbreak_phones:
        disease = get_disease(disease_list)
        if phone.number in test_phones:
            test_phones.remove(phone.number)
        report_type = head_count_or_deaths()
        cases = case_count_percent_change_generator(report_type, 1.5)
        message_body = report_type + "; " + disease + "; " + str(cases)
        data.append([phone.number, message_body, data_date])
        
    for phone in test_phones:
        disease = get_disease(disease_list)
        report_type = head_count_or_deaths()
        cases = case_count_generator(report_type)
        message_body = report_type + "; " + disease + "; " + str(cases)
        data.append([phone.number, message_body, data_date])
    
    date_now = dt.now().strftime('%m%d%Y%I%M%S%f')
    with open('test-data-'+date_now+'.csv', 'w', newline='') as outfile:
        outwriter = csv.writer(outfile, delimiter=',')
        outwriter.writerows(data) 

#save the test data to a file. Utilizes the get_disease_outbreak function which
#increases the probability of seeing a specific disease
def write_test_data_disease(count, data_date, disease_name):
    phone_list = generate_phone_numbers(count)
    hosp_choices = LHCP.objects.all().count() - 1
    disease_list = Diseases.objects.all().count()
    
    for phone_num in phone_list:
        associate_phone_location(phone_num, hosp_choices)
    
    test_phones = phones_for_data(count)
    
    data = []
    for phone in test_phones:
        disease = get_outbreak_disease(disease_list, disease_name)
        report_type = head_count_or_deaths()
        cases = case_count_generator(report_type)
        message_body = report_type + "; " + disease + "; " + str(cases)
        data.append([phone.number, message_body, data_date])
    
    date_now = dt.now().strftime('%m%d%Y%I%M%S%f')
    with open('test-data-'+date_now+'.csv', 'w', newline='') as outfile:
        outwriter = csv.writer(outfile, delimiter=',')
        outwriter.writerows(data) 


#grabs a random disease but increases the probability of seeing a specified
#disease (given by the variable outbreak_disease)
def get_outbreak_disease(diseases_count, outbreak_disease):
    if random.uniform(0,1) < 0.4:
        return Diseases.objects.filter(name=outbreak_disease).first().name
    else:
        idx = random.randint(0, diseases_count - 1)
        return Diseases.objects.all()[idx].name
    

#generates a random number of cases that is offset by the mean shift
def case_count_mean_shift_generator(h_or_d, mean_shift):
    i = mean_shift
    j = math.sqrt(mean_shift)
    
    added_randomness = random.uniform(0,1)
    if h_or_d == "H":
        if added_randomness < 0.5:
            count = random.normalvariate(20+i,3*j)
        elif added_randomness < 0.75:
            count = random.normalvariate(50+i,5*j)
        else:
            count = random.normalvariate(100+i, 10*j)
    else:
        if added_randomness < 0.7:
            count = random.normalvariate(3+i,1*j)
        elif added_randomness < 0.9:
            count = random.normalvariate(7+i,2*j)
        else:
            count = random.normalvariate(100+i,10*j)
    return round(count)

#generate a case count based on percentage change
def case_count_percent_change_generator(h_or_d, multiplier):
    i = multiplier
    added_randomness = random.uniform(0,1)
    if h_or_d == "H":
        if added_randomness < 0.5:
            count = random.normalvariate(20*i,3)
        elif added_randomness < 0.75:
            count = random.normalvariate(50*i,5)
        elif added_randomness > 0.999:
            count = random.normalvariate(1000*i,50)
        else:
            count = random.normalvariate(100*i, 10)
    else:
        if added_randomness < 0.7:
            count = random.normalvariate(3*i,1)
        elif added_randomness < 0.9:
            count = random.normalvariate(7*i,2)
        elif added_randomness > 0.9999:
            count = random.normalvariate(10000*i,1000)
        else:
            count = random.normalvariate(100*i,10)
    return round(count)

#increment date
def increment_date(add_options, day):
    date = add_options['start'] + td(days=day)
    return date.strftime(Command.date_format)