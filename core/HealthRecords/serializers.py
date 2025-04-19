from rest_framework import serializers
from .models import Immunization,BloodTest,Disease,MRIRecord
from datetime import datetime

class Immunization_Serializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    to_be_used_by=serializers.CharField(source="user.username", read_only=True) 
    class Meta: 
        model=Immunization
        fields=['id','user','vaccine_name','date','next_daose_reminder','to_be_used_by']
        read_only_fields = ["user"]


    def validate_next_daose_reminder(self, value):
        """Ensure that next dose reminder is after the vaccination date."""
        if "date" in self.initial_data:  
            try:
                # Convert string to datetime.date
                vaccine_date = datetime.strptime(self.initial_data.get("date"), "%Y-%m-%d").date()
            except ValueError:
                raise serializers.ValidationError("Invalid date format for vaccine date. Use YYYY-MM-DD.")

            if value < vaccine_date:
                raise serializers.ValidationError("Next dose reminder must be after the vaccine date.")

        return value

class BloodTest_Serializer(serializers.ModelSerializer):  
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    to_be_used_by=serializers.CharField(source="user.username", read_only=True) 

    class Meta:
        model = BloodTest
        fields = ['id', 'user', 'test_date', 'test_results', 'notes','to_be_used_by','test_name']  
        read_only_fields = ["user"]


class DiseaseSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    to_be_used_by=serializers.CharField(source="user.username", read_only=True) 
    class Meta:
        model = Disease
        fields = ['id', 'user', 'name', 'diagnosis_date', 'severity', 'is_active', 'notes','to_be_used_by','doctor_name','doctor_phone']
        read_only_fields = ['id', 'user']  # The user should be set automatically

    def validate_diagnosis_date(self, value):

        from datetime import date
        if value > date.today():
            raise serializers.ValidationError("Diagnosis date cannot be in the future.")
        return value

class MRIRecordSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    to_be_used_by=serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = MRIRecord
        fields = ['id', 'user', 'scan_type', 'scan_date', 'image', 'report', 'notes','to_be_used_by','doctor_name','doctor_phone']




