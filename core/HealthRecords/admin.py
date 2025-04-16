from django.contrib import admin
from .models import Immunization, BloodTest, Disease, MRIRecord

@admin.register(Immunization)
class ImmunizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'vaccine_name', 'date', 'next_daose_reminder')
    search_fields = ('user__username', 'vaccine_name')
    list_filter = ('date', 'next_daose_reminder')

@admin.register(BloodTest)
class BloodTestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'test_name', 'test_date')
    search_fields = ('user__username', 'test_name')
    list_filter = ('test_date',)
    ordering = ['-test_date']

@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'diagnosis_date', 'severity', 'is_active')
    search_fields = ('user__username', 'name')
    list_filter = ('severity', 'is_active', 'diagnosis_date')
    ordering = ['-diagnosis_date']

@admin.register(MRIRecord)
class MRIRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'scan_type', 'scan_date', 'doctor_name', 'doctor_phone')
    search_fields = ('user__username', 'scan_type', 'doctor_name')
    list_filter = ('scan_date',)
    ordering = ['-scan_date']
