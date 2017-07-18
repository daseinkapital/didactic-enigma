from django.core.management.base import BaseCommand
from map.models import Districts, Reports

import csv

class Command(BaseCommand):
    args = '<none really>'
    help = 'Read district data in to the database.'
    
    def handle(self, *args, **options):
        Districts.objects.all().delete()
        with open('district_info.csv', 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=',')
                for row in reader:
                    print(row)  
                    Districts.objects.create(
                            name = row['Name'],
                            latitude = row['Lat'],
                            longitude = row['Lng']
                            )