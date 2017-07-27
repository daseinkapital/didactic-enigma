from django.core.management.base import BaseCommand
from map.models import LHCP, Phones, Diseases

from datetime import datetime as dt
from datetime import timedelta as td
import random
import csv
import os

class Command(BaseCommand):
    args = '<none really>'
    help = 'Generates test data'
    
    #This is a global format for date parsing. If the date ever changes, change it here and it will
    #be reflected all through out the document
    date_format = '%Y-%m-%d'
    
    #allow the user to specify switches for the mgmt command
    def add_arguments(self, parser):
        parser.add_argument(
                '--days',
                nargs=1,
                type=int,
                default=1,
                help='Create data for a specified number of days (int)'
            )
        
        parser.add_argument(
                '--date',
                nargs=1,
                type=str,
                default = dt.today().strftime(Command.date_format),
                help='Pick a specific day to generate data on (strf '+Command.date_format+')'
            )
        
        parser.add_argument(
                '--dates',
                nargs=2,
                type=str,
                help = 'Choose two days to generate a range of data from (strf '+Command.date_format+')'
            )
        
        parser.add_argument(
                '--count',
                action='store',
                type=int,
                default=500,
                help = 'Specify the number of randomly generated data points for each day (defaults to 500)'
            )
        
        parser.add_argument(
                '--random-data',
                nargs=2,
                type=int,
                help='Generate a random number of test data lines (enter a lower and upper int bound)'
            )
        
        parser.add_argument(
                '--supress',
                action='store_true',
                dest='supress',
                default=False,
                help='Supress print statements'
            )
        
        parser.add_argument(
                '--no-dir-change',
                action='store_true',
                dest='no-dir-change',
                default=False,
                help='Don\'t change the working directory'
            )
        
        parser.add_argument(
                '--test-supress',
                action='store_true',
                dest='test-supress',
                default=False,
                help='Supress the done statement for testing purposes'
            )
        
    
    #main function control
    def handle(self, *args, **options):
            #save test data to a testdata folder
            if not options['no-dir-change']:
                os.chdir(os.getcwd() + '\\testdata')
            
            #if dates are specified, override any day/single date option
            if options['dates']:
                options['days'] = None
                options['date'] = None 
                
            #if the random switch is used, remove any given count
            if options['random_data']:
                options['count'] = None
                options.update({'lower': min(options['random_data']), 'upper': max(options['random_data'])})
            
            #if multiple dates option is selected, parse the dates and determine how many times
            #to create data
            if options['dates']:
                dates = options['dates']
                start_date = dt.strptime(dates[0], Command.date_format)
                end_date = dt.strptime(dates[1], Command.date_format)
                delta = end_date - start_date
                num_days = delta.days + 1
                loop_days(start_date, num_days, options)

            #if the number of days are specified, generate enough points for the number specified
            elif options['days']:
                #if the date option is the default value (today), create data going back the number
                #of days specified to today (-1s added for date adjustments)
                if options['date'] == dt.today().strftime(Command.date_format):
                    start_date = dt.today() - td(days=options['days'] - 1)
                    num_days = options['days'] - 1
                    loop_days(start_date, num_days, options)
                
                #if the date switch was specified then start at that date, and create an appropriate
                #number of files as specified 
                else:
                    date_str = options['date']
                    start_date = dt.strptime(date_str[0], Command.date_format)
                    num_days = options['days'] - 1
                    loop_days(start_date, num_days, options)
            if not options['test-supress']:
                print('Done.')

#generate test data with the given options from the start date. Start date must be a datetime object,
#num_days is an integer (0 if only 1 day) and options is the list of options generated by the mgmt
#command
def loop_days(start_date, num_days, options):
    for i in range(num_days + 1):
        day = start_date + td(days=i)
        day_str = day.strftime(Command.date_format)
        #if random is selected, generate a random count of data points to be created that
        #day before calling the function
        if options['random_data']:
            count = random.randint(options['lower'], options['upper'])
            write_test_data(count, day_str)
            if not options['supress']:
                print("Data created for "+ day.strftime(Command.date_format))
            
        #if random wasn't select, default to the count
        else:
            write_test_data(options['count'], day_str)
            if not options['supress']:
                print("Data created for "+ day.strftime(Command.date_format))
                    
                    
#save the test data to the file
def write_test_data(count, data_date):
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
        cases = case_count_generator(report_type)
        message_body = report_type + "; " + disease + "; " + str(cases)
        data.append([phone.number, message_body, data_date])
    
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