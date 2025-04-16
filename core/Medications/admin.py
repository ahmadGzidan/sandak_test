from django.contrib import admin
from .models import Medications

class MedicationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'storage', 'dosage', 'start_date', 'end_date')

admin.site.register(Medications, MedicationsAdmin)