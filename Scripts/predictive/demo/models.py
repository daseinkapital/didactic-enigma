from django.db import models


# Create your models here.
name_length = 250
    

class Reports(models.Model):
    date = models.DateField(
            auto_now=False,
            auto_now_add=False,
        )
    
    phone_number = models.ForeignKey(
            'Phones',
            on_delete=models.CASCADE
        )
    
    disease = models.ForeignKey(
            'Diseases',
            on_delete=models.CASCADE
        )
    
    report_num = models.AutoField(
            primary_key=True,
        )
    

class HeadReports(Reports):
    count = models.IntegerField(
            null=False
        )
    
class DeathReports(Reports):
    count = models.IntegerField(
            null=False
        )
    
    
class Phones(models.Model):
    number = models.CharField(
            primary_key=True,
            max_length = name_length
        )
    
    lat = models.FloatField(
            null=False
        )
    
    lng = models.FloatField(
            null=False
        )
    
    
#class Alerts(models.Model):
#    lhcp = models.ForeignKey(
#            'LHCP',
#            on_delete = models.CASCADE
#        )
#    
#    alert_num = models.AutoField(
#            primary_key=True
#        )
    
    
class Diseases(models.Model):
    name = models.CharField(
            primary_key=True,
            max_length = name_length
        )
    

class AltDiseases(models.Model):
    alt_name = models.CharField(
            primary_key=True,
            max_length = name_length
        )
    
    official_name = models.ForeignKey(
            'Diseases',
            on_delete=models.CASCADE
        )