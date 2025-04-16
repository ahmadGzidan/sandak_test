from rest_framework import serializers
from .models import Medications

class Medications_Serializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    to_be_used_by=serializers.CharField(source="user.username", read_only=True) 
    class Meta:
        model = Medications
        fields = [
            "id",
            "user",
            "name",
            "storage",
            "dosage",
            "time_in_a_day",
            "pills_in_a_time",
            "start_date",
            "end_date",
            "to_be_used_by"
        ]
        read_only_fields = ["user"]

    def validate(self, data):
        """Ensure start_date is before end_date"""
        if data["start_date"] > data["end_date"]:
            raise serializers.ValidationError({"error": "Start date must be before end date."})
        return data
