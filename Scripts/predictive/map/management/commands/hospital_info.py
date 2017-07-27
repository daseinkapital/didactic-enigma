from django.core.management.base import BaseCommand

import csv

from map.models import LHCP, Districts

class Command(BaseCommand):
    args = '<none>'
    help = 'Populate database with hospital data'
    
    def handle(self, *args, **options):
        LHCP.objects.all().delete()
        with open('Health Facilities - Sierra Leone.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            lat = []
            lng = []
            district = []
            center_id = []
            for row in reader:
                lat.append(row['Lat'])
                lng.append(row['Long'])
                district.append(row['District'])
                center_id.append(row['Centre ID'])
            for idx in range(len(lat)):
                if lat[idx] != "":
                    if lng[idx] != "":
                        if district[idx] != "":
                            if 'Urban' or 'Rural' in district[idx]:
                                if 'Urban' in district[idx]:
                                    LHCP.objects.create(
                                            name = center_id[idx],
                                            lat = lat[idx],
                                            lng = lng[idx],
                                            district = Districts.objects.filter(name__icontains="Urban").first(),
                                        )
                                else:
                                    LHCP.objects.create(
                                            name = center_id[idx],
                                            lat = lat[idx],
                                            lng = lng[idx],
                                            district = Districts.objects.filter(name__icontains="Rural").first(),
                                        )

                            else:
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
            LHCP.objects.all().count()