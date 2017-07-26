from django.core.management.base import BaseCommand

import csv
import os

from map.models import Phones, HeadReports, DeathReports, AltDiseases

class Command(BaseCommand):
    args = '<None>'
    help = "Reads in fake generated data to the database"
    
    #loop over all files in ./testdata and read them in to reports
    def handle(self, *args, **options):
        HeadReports.objects.all().delete()
        DeathReports.objects.all().delete()
        os.chdir(os.getcwd() + '\\testdata')
        for root, dirs, files in os.walk(os.getcwd()):
            for file in files:
                with open(file, 'r') as data:
                    reader = csv.reader(data)
                    for row in reader:
                        report_type, disease, count = parse_SMS(row[1])
                        if report_type == "H":
                            HeadReports.objects.create(
                                date = row[2],
                                phone_number = Phones.objects.filter(number = parse_Phone(row[0])).first(),
                                disease = AltDiseases.objects.filter(alt_name__iexact=disease).first().official_name,
                                count = count
                            )
                        elif report_type == "D":
                            DeathReports.objects.create(
                                date = row[2],
                                phone_number = Phones.objects.filter(number = parse_Phone(row[0])).first(),
                                disease = AltDiseases.objects.filter(alt_name__iexact=disease).first().official_name,
                                count = count
                            )
                        else:
                            print("Invalid report type: " + report_type)

#numbers from CSV are not 0 padded, so add appropriate 0s                        
def parse_Phone(phone_num):
    padding = 7 - len(phone_num)
    return "0"*padding + phone_num

#parse the message
def parse_SMS(message):
    report_type, disease, count = message.split(';')
    report_type = report_type.strip()
    disease = disease.strip()
    count = count.strip()
    return report_type, disease, count