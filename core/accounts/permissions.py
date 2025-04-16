from rest_framework import permissions
from accounts.models import FamilyMember  # Import FamilyMember model

class IsElderlyOrFamilyMember(permissions.BasePermission):
    """
    Custom permission to allow only the elderly user or their approved family members
    to manage medications.
    """

    def has_object_permission(self, request, view, obj):
        # Allow if the user is the owner of the medication
        if obj.user == request.user:
            return True

        # Allow if the user is a family member of the medication owner
        return FamilyMember.objects.filter(user=obj.user, family_member=request.user).exists()
