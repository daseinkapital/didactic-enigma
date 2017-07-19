from django.core.management.base import BaseCommand
from map.models import Districts

import csv

class Command(BaseCommand):
    args = '<none really>'
    help = 'Read district data in to the database.'
    
    def add_arguments(self, parser):
        parser.add_argument(
                '--override',
                action='store_true',
                dest='override',
                default=False,
                help='Override existing models with new data if the models already exist.')
    
    def handle(self, *args, **options):
        Districts.objects.all().delete()
        with open('district_info.csv', 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=',')
                for row in reader:
                    exists = Districts.objects.filter(name=row['Name']).first()
                    if options['override']:
                        if exists:
                            exists.delete()
                        Districts.objects.create(
                            name = row['Name'],
                            lat = row['Lat'],
                            lng = row['Lng'],
                            zoom = row['Zoom']
                            )
                    else:
                        if exists:
                            pass                        
                        else:
                            Districts.objects.create(
                                    name = row['Name'],
                                    lat = row['Lat'],
                                    lng = row['Lng'],
                                    zoom = row['Zoom']
                                    )