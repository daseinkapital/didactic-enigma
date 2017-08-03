from django.db import models


# Create your models here.
name_length = 250
    

class Reports(models.Model):
    date = models.DateField(
            auto_now_add=True
        )
    
    phone_number = models.ForeignKey(
            'Phones',
            on_delete=models.CASCADE
        )
    
    disease = models.CharField(
            max_length=name_length
        )
    
    report_num = models.AutoField(
            primary_key=True,
        )
    
    count = models.IntegerField(
            null=False
        )
    
    
class Phones(models.Model):
    number = models.CharField(
            primary_key=True,
            max_length=name_length
        )
    
    code = models.ForeignKey(
            'Cities',
            on_delete=models.CASCADE
        )
        
class Cities(models.Model):
    name = models.CharField(
            max_length=name_length
        )

    code = models.IntegerField(
            null=False,
        )
    
    lat = models.FloatField(
            null=False
        )
    
    lng = models.FloatField(
            null=False
        )
    
    state_code = models.CharField(
            max_length=name_length
        )
    
    name_state = models.CharField(
            primary_key=True,
            max_length=name_length
        )
    
