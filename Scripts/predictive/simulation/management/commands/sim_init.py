from django.core.management.base import BaseCommand

import csv

from simulation.models import Diseases, AltDiseases, Districts, LHCP

class Command(BaseCommand):
    args = '<none really>'
    help = 'Populates the database with the district info, disease info, and hospital info.'
    
    def add_arguments(self, parser):
        parser.add_argument(
                '--district-override',
                action='store_true',
                dest='override',
                default=False,
                help='Override existing models with new data if the models already exist.'
            )
    
    def handle(self, *args, **options):
        #district data read in
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
        
        #hospital data read in
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
        
        #disease data read in
        Diseases.objects.all().delete()
        AltDiseases.objects.all().delete()
        with open('disease_info.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            alt_names = []
            names = []
            for row in reader:
                alt_names.append([row['Alternative Names'], row['Disease Names']])
                names.append(row['Disease Names'])
            unique_names = list(set(names))
            
            for name in unique_names:
                Diseases.objects.create(
                        name = name
                    )
            
            for row in alt_names:
                AltDiseases.objects.create(
                        alt_name = row[0],
                        official_name = Diseases.objects.filter(name=row[1]).first()
                )