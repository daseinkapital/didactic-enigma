from django.db import models


# Create your models here.
name_length = 250


class Districts(models.Model):
    name = models.CharField(
            max_length=name_length,
            primary_key=True
        )
    
    lng = models.FloatField()
    
    lat = models.FloatField()
    
    #can we change this?
    zoom = models.IntegerField()
    

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


class LHCP(models.Model):
    name = models.CharField(
            max_length = name_length
        )
    
    lat = models.FloatField(
            null=False
        )
    
    lng = models.FloatField(
            null=False
        )
    
    district = models.ForeignKey(
            'Districts',
            on_delete=models.CASCADE
        )
    
    code = models.AutoField(
            primary_key=True
        )
    
    
class Phones(models.Model):
    number = models.CharField(
            primary_key=True,
            max_length = name_length
        )
    
    hospital = models.ForeignKey(
            'LHCP',
            on_delete=models.CASCADE
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
    