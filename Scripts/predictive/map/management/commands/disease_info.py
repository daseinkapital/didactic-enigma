from django.core.management.base import BaseCommand

import csv

from map.models import Diseases, AltDiseases

class Command(BaseCommand):
    args = '<none>'
    help = 'Populate database with hospital data'
    
    def handle(self, *args, **options):
        with open('disease_info.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            print(reader)