from django.db import models


# Create your models here.
name_length = 250



class Districts(models.Model):
    name = models.CharField(
            max_length=name_length
        )
    
    longitude = models.DecimalField(
            max_digits=6,
            decimal_places=3
        )
    
    latitude = models.DecimalField(
            max_digits=6,
            decimal_places=3
        )
    
#    zoom = models.IntegerField()
#    
#    latBnd = models.FloatField()
#    
#    lngBnd = models.FloatField()
    

class Reports(models.Model):
    district = models.ForeignKey(
            'Districts',
            on_delete=models.CASCADE
        )
    
    date = models.DateField(
            auto_now=False,
            auto_now_add=False,
        )
    
    population = models.IntegerField()
    
    new_cnfmd = models.IntegerField()
    
    cum_cnfmd = models.IntegerField()
    
    death_cnfmd = models.IntegerField()