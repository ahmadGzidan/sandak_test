from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from .models import Medications
from .serializers import Medications_Serializer
from accounts.permissions import IsElderlyOrFamilyMember
from accounts.models import Account, FamilyMember
from .utils.interaction_check import check_medication_interactions

#  List Medications (Only show user's own medications or their elderly family members' medications)
class ListMedicationsView(generics.ListAPIView):
    serializer_class = Medications_Serializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter medications to show only those of the logged-in user or their elderly family members."""
        user = self.request.user

        # Get IDs of elderly family members where the user is an approved family member
        family_member_ids = FamilyMember.objects.filter(
            family_member=user
        ).values_list("user_id", flat=True)

        # Get medications for the user and their elderly family members (ensuring distinct results)
        return Medications.objects.filter(user__in=[user.id, *family_member_ids]).distinct().prefetch_related("user")



class MedicationsDetailView(generics.RetrieveAPIView):
    serializer_class = Medications_Serializer
    queryset = Medications.objects.all()  

    def get_object(self):
        """Retrieve a medication only if it belongs to the user or their elderly family members."""
        medication = super().get_object()  # Get the requested medication
        user = self.request.user

        # Get IDs of elderly family members where the user is an approved family member
        family_member_ids = FamilyMember.objects.filter(
            family_member=user
        ).values_list("user_id", flat=True)

        # Check if the medication belongs to the user or their elderly family members
        if medication.user.id not in [user.id, *family_member_ids]:
            raise PermissionDenied("You do not have permission to view this medication.")

        return medication


class MedicationsCreateView(generics.CreateAPIView):
    queryset = Medications.objects.all()
    serializer_class = Medications_Serializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        elderly_user_id = self.request.data.get("elderly_user_id")
        new_med = self.request.data.get("name")  # Get new med name

        if elderly_user_id:
            try:
                elderly_user = Account.objects.get(id=elderly_user_id)
            except Account.DoesNotExist:
                raise ValidationError({"error": "Elderly user not found."})

            is_family_member = FamilyMember.objects.filter(
                user=elderly_user, family_member=self.request.user
            ).exists()

            if not is_family_member and elderly_user != self.request.user:
                raise PermissionDenied("You do not have permission to add medication for this user.")

            user = elderly_user
        else:
            user = self.request.user

        # Fetch existing meds for the user
        existing_meds = Medications.objects.filter(user=user).values_list('name', flat=True)

        # Check for interactions
        warnings = check_medication_interactions(new_med, existing_meds)

        if warnings:
            raise ValidationError({
                "interaction_warnings": warnings
            })

        # If no issues, save
        serializer.save(user=user)

#  Update Medication (Only if the user is the owner or an approved family member)
class MedicationsUpdateView(generics.UpdateAPIView):
    queryset = Medications.objects.all()
    serializer_class = Medications_Serializer
    permission_classes = [IsAuthenticated, IsElderlyOrFamilyMember]

    def perform_update(self, serializer):
        """Ensure only the medication owner or their approved family members can update."""
        medication = self.get_object()
        elderly_user_id = self.request.data.get("elderly_user_id")

        # Check if user is the owner or an approved family member
        is_family_member = FamilyMember.objects.filter(
            user=medication.user, family_member=self.request.user
        ).exists()

        if not is_family_member and medication.user != self.request.user:
            raise PermissionDenied("You do not have permission to update this medication.")

        if elderly_user_id:  # If updating a family member's medication
            try:
                elderly_user = Account.objects.get(id=elderly_user_id)
            except Account.DoesNotExist:
                raise ValidationError({"error": "Elderly user not found."})

            # Ensure the authenticated user is a family member of the elderly user
            if not FamilyMember.objects.filter(user=elderly_user, family_member=self.request.user).exists():
                raise PermissionDenied("You do not have permission to update medication for this user.")

            # Save the medication for the elderly user but keep ownership unchanged
            serializer.save(user=medication.user)  

        else:  
            # Update medication for the authenticated user
            serializer.save()


#  Delete Medication (Only if the user is the owner or an approved family member)
class MedicationsDeleteView(generics.DestroyAPIView):
    queryset = Medications.objects.all()
    serializer_class = Medications_Serializer
    permission_classes = [IsAuthenticated, IsElderlyOrFamilyMember]

    def get_object(self):
        """Retrieve a medication only if it belongs to the user or their elderly family members."""
        medication = super().get_object()
        user = self.request.user

        # Get IDs of elderly family members where the user is an approved family member
        family_member_ids = FamilyMember.objects.filter(
            family_member=user
        ).values_list("user_id", flat=True)

        # Check if the medication belongs to the user or their elderly family members
        if medication.user.id not in [user.id, *family_member_ids]:
            raise PermissionDenied("You do not have permission to delete this medication.")

        return medication