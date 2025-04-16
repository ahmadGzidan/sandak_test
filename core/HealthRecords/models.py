from django.db import models
from accounts.models import Account

# Create your models here.

class Immunization(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    vaccine_name=models.CharField(max_length=30)
    date=models.DateField()
    next_daose_reminder=models.DateField()

    def __str__(self):
        return f"{self.vaccine_name} - {self.user.username}"  # Fix here

class BloodTest(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=50)
    test_date = models.DateField()
    test_results =models.JSONField(default=dict) 
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.test_name} - {self.user.username} ({self.test_date})"

    class Meta:
        ordering = ["-test_date"]

class Disease(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="diseases")  # Link to user
    name = models.CharField(max_length=100)  # Disease name
    diagnosis_date = models.DateField()  # Date when the disease was diagnosed
    severity = models.CharField(max_length=20)
    notes = models.TextField(blank=True, null=True)
     # Additional doctor notes or user notes
    is_active = models.BooleanField(default=True)  # Whether the disease is ongoing or resolved
    doctor_name = models.CharField(max_length=100, blank=True, null=True)  # New field
    doctor_phone = models.CharField(max_length=20, blank=True, null=True)  # New field
    def __str__(self):
        return f"{self.name} ({self.user.username})"
    
class MRIRecord(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="mri_records")
    scan_type = models.CharField(max_length=100)  # Example: Brain MRI, Spine MRI
    scan_date = models.DateField()
    image = models.ImageField(upload_to="mri_scans/")
    report = models.TextField(blank=True, null=True)  # Radiologist's report
    notes = models.TextField(blank=True, null=True)
    doctor_name = models.CharField(max_length=100, blank=True, null=True)  # New field
    doctor_phone = models.CharField(max_length=20, blank=True, null=True)  # New field

    def __str__(self):
        return f"{self.scan_type} - {self.user.username} ({self.scan_date})"
    
