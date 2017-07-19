from django.core.management.base import BaseCommand

import csv

from map.models import Diseases, AltDiseases

class Command(BaseCommand):
    args = '<none>'
    help = 'Populate database with hospital data'
    
    def handle(self, *args, **options):
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