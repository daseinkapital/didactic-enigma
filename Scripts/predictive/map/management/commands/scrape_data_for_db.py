from django.core.management.base import BaseCommand
from map.models import Districts, Reports

from os import walk
import csv
from datetime import datetime as dt

class Command(BaseCommand):
    args = '<none really>'
    help = 'Grab all the csvs available and read them in to the database.'
    
    def handle(self, *args, **options):
        sl_data = 'sl_data'
        f = []
        for (dirpath, dirnames, filenames) in walk(sl_data):
            f.extend(filenames)
            break

        good_data = []
        for file in f:
            if file[0:1] == '2':
                good_data.append(sl_data + '/' + file)

        district_objs = Districts.objects.all()
        district_names = []
        for district in district_objs:
            district_names.append(district.name)
        print(district_names)

        for file in good_data:
            with open(file, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=',')
                interestingrows = [row for idx, row in enumerate(reader) if idx in (0, 4, 8, 11)]
                for district_name in district_names:
                    district = Districts.objects.filter(name=district_name).first()
                    
                    date_string = file[8:18]
                    date = dt.strptime(date_string, '%Y-%m-%d')
                    
                    pop_data = interestingrows[0]
                    new_confd_data = interestingrows[1]
                    cum_confd_data = interestingrows[2]
                    death_confd_data = interestingrows[3]
                    
                    pop = CountryValue(pop_data, district_name)
                    new_confd = CountryValue(new_confd_data, district_name)
                    cum_confd = CountryValue(cum_confd_data, district_name)
                    death_confd = CountryValue(death_confd_data, district_name)
                    
                    pop = CorrectValue(pop)
                    new_confd = CorrectValue(new_confd)
                    cum_confd = CorrectValue(cum_confd)
                    death_confd = CorrectValue(death_confd)
                    
                    
                    Reports.objects.create(
                            district=district,
                            date=date,
                            population=pop,
                            new_cnfmd=new_confd,
                            cum_cnfmd=cum_confd,
                            death_cnfmd=death_confd
                        )

def CountryValue(OrderedDict, country_name):
    if 'Western' in country_name:
        return OrderedDict[UpperFirst(country_name)]
    else:
        return OrderedDict[country_name]
    
def CorrectValue(value):
    if value == '':
        return 0
    else:
        return int(value.replace(',',''))

def UpperFirst(string):
    return string[0].upper() + string[1:].lower()
                    
            
    
        