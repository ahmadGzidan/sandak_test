from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import Account



class Medications(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    name = models.CharField(max_length=40, blank=False, null=False)
    storage = models.IntegerField(default=0, blank=False, null=False)
    dosage= models.CharField(max_length=40,blank=False, null=False,default='0')
    time_in_a_day=models.JSONField(default=dict)
    pills_in_a_time=models.IntegerField(blank=False, null=False,default='0')
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)



    def __str__(self):
        return self.name