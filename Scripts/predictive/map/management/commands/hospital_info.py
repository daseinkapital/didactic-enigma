from django.core.management.base import BaseCommand

import csv

from map.models import LHCP, Districts

class Command(BaseCommand):
    args = '<none>'
    help = 'Populate database with hospital data'
    
    def handle(self, *args, **options):
        with open('Health Facilities - Sierra Leone.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for row in reader:
                lat = row['Lat']
                lng = row['Lng']
                district = row['District']
                center_id = row['Center ID']
            for idx in enumerate(reader):
                if lat[idx] != "":
                    if lng[idx] != "":
                        if district != "":
                            LHCP.objects.create(
                                    name = center_id[idx],
                                    lat = lat[idx],
                                    lng = lng[idx],
                                    district = Districts.objects.filter(name=district[idx]).first(),
                                )
                        else:
                            pass
                    else:
                        pass
                else:
                    pass