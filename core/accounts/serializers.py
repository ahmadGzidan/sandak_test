from rest_framework import serializers
from .models import Account, FamilyMember

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    age = serializers.ReadOnlyField() 
    
    class Meta:
        model = Account
        fields = ["id","email", "username", "password", "password2", "first_name", "last_name","age","gender",'personal_image','date_of_birth']
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        personal_image = self.validated_data.get("personal_image", None)
        account = Account(
            email=self.validated_data["email"],
            username=self.validated_data["username"],
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            gender=self.validated_data["gender"],
            date_of_birth=self.validated_data["date_of_birth"],
            personal_image=personal_image

        )
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})

        account.set_password(password)
        account.save()
        return account

class FamilyMemberSerializer(serializers.ModelSerializer):
    family_member_username = serializers.CharField(write_only=True)  
    user_username = serializers.CharField(source="user.username", read_only=True)  
    family_member_username_display = serializers.CharField(source="family_member.username", read_only=True)  # Add username for family member

    class Meta:
        model = FamilyMember
        fields = [
            "id",
            "user_id",
            "family_member_username",
            "user_username",  
            "family_member_id",
            "family_member_username_display",  
            "relationship_type",
            "added_at",
        ]
        read_only_fields = ["user", "family_member", "added_at", "user_username", "family_member_username_display"]


    def create(self, validated_data):
        request = self.context.get("request")
        if not request:
            raise serializers.ValidationError({"error": "Request context is missing."})

        user = request.user  # The logged-in user
        family_member_username = validated_data.pop("family_member_username", None)

        if not family_member_username:
            raise serializers.ValidationError({"family_member_username": "This field is required."})

        # Check if the family member exists
        try:
            family_member = Account.objects.get(username=family_member_username)
        except Account.DoesNotExist:
            raise serializers.ValidationError({"family_member": "User not found."})

        # Prevent adding oneself
        if user == family_member:
            raise serializers.ValidationError({"family_member": "You cannot add yourself as a family member."})

        # Prevent duplicate relationships
        if FamilyMember.objects.filter(user=user, family_member=family_member).exists():
            raise serializers.ValidationError({"family_member": "This user is already a family member."})

        # Explicitly set user and family_member instead of passing them in validated_data
        family_member_obj = FamilyMember.objects.create(
            user=user, family_member=family_member, relationship_type=validated_data["relationship_type"]
        )

        return family_member_obj
    


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "email", "username", "first_name", "last_name", "date_of_birth", "gender", "age", "personal_image", "phone_number"]
        read_only_fields = ["email", "username", "gender"]
