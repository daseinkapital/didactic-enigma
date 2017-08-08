from django.core.management.base import BaseCommand
from demo.models import Cities

import csv

class Command(BaseCommand):
    args = '<none really>'
    help = 'Load information about city locations and the area codes that are covered by them'
    

    #allow the user to specify switches for the mgmt command
    def add_arguments(self, parser):
        parser.add_argument(
                '--days',
                nargs=1,
                type=int,
                default=[1],
                help='Create data for a specified number of days (int)'
            )
        
        
    
    #main function control
    def handle(self, *args, **options):
        Cities.objects.all().delete()
        with open('us-area-code-cities.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            dbl_check = []
            for row in reader:
                print(row)
                name_state = row[1] + ", " + row[2] + " (" + row[0] + ")"
                if name_state not in dbl_check:
                    Cities.objects.create(
                            name=row[1],
                            code=row[0],
                            lat=row[4],
                            lng=row[5],
                            state_code=row[2],
                            name_state=name_state
                        )
                dbl_check.append(name_state)