from django.shortcuts import render
from .models import Immunization, BloodTest,Disease,MRIRecord
from .serializers import Immunization_Serializer, BloodTest_Serializer,DiseaseSerializer,MRIRecordSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsElderlyOrFamilyMember  
from accounts.models import FamilyMember, Account
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404


# 📌 List all Immunizations
class List_Immunization(generics.ListAPIView):
    queryset = Immunization.objects.all()
    serializer_class = Immunization_Serializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve only immunizations belonging to the user or their elderly family members."""
        user = self.request.user
        family_member_ids = FamilyMember.objects.filter(
            family_member=user
        ).values_list("user_id", flat=True)

        return Immunization.objects.filter(user__in=[user.id, *family_member_ids]).distinct().prefetch_related("user")


# 📌 Retrieve a Specific Immunization
class ImmunizationDetailView(generics.RetrieveAPIView):
    queryset = Immunization.objects.all()
    serializer_class = Immunization_Serializer
    permission_classes = [IsAuthenticated, IsElderlyOrFamilyMember]

    def get_object(self):
        """Retrieve an immunization only if it belongs to the user or their elderly family members."""
        immunization = super().get_object()
        user = self.request.user

        family_member_ids = FamilyMember.objects.filter(
            family_member=user
        ).values_list("user_id", flat=True)

        if immunization.user.id not in [user.id, *family_member_ids]:
            raise PermissionDenied("You do not have permission to view this immunization.")

        return immunization


# 📌 Add Immunization (Elderly User or Family Member)
class ImmunizationCreateView(generics.CreateAPIView):
    queryset = Immunization.objects.all()
    serializer_class = Immunization_Serializer
    permission_classes = [IsAuthenticated, IsElderlyOrFamilyMember]

    def perform_create(self, serializer):
        """Allow a user to add immunization for themselves or an elderly family member."""
        elderly_user_id = self.request.data.get("elderly_user_id")

        if elderly_user_id:
            try:
                elderly_user = Account.objects.get(id=elderly_user_id)
            except Account.DoesNotExist:
                raise ValidationError({"error": "Elderly user not found."})

            is_family_member = FamilyMember.objects.filter(
                user=elderly_user, family_member=self.request.user
            ).exists()

            if not is_family_member and elderly_user != self.request.user:
                raise PermissionDenied("You do not have permission to add immunization for this user.")

            serializer.save(user=elderly_user)
        else:
            serializer.save(user=self.request.user)


# 📌 Update Immunization (Only Elderly User or Family Members)
class ImmunizationUpdateView(generics.UpdateAPIView):
    queryset = Immunization.objects.all()
    serializer_class = Immunization_Serializer
    permission_classes = [IsAuthenticated, IsElderlyOrFamilyMember]

    def perform_update(self, serializer):
        """Ensure only the immunization owner or their approved family members can update."""
        immunization = self.get_object()
        elderly_user_id = self.request.data.get("elderly_user_id")

        is_family_member = FamilyMember.objects.filter(
            user=immunization.user, family_member=self.request.user
        ).exists()

        if not is_family_member and immunization.user != self.request.user:
            raise PermissionDenied("You do not have permission to update this immunization.")

        if elderly_user_id:
            try:
                elderly_user = Account.objects.get(id=elderly_user_id)
            except Account.DoesNotExist:
                raise ValidationError({"error": "Elderly user not found."})

            if not FamilyMember.objects.filter(user=elderly_user, family_member=self.request.user).exists():
                raise PermissionDenied("You do not have permission to update immunization for this user.")

            serializer.save(user=immunization.user)  # Keep ownership unchanged
        else:
            serializer.save()


# 📌 Delete Immunization (Only Elderly User or Family Members)
class ImmunizationDeleteView(generics.DestroyAPIView):
    queryset = Immunization.objects.all()
    serializer_class = Immunization_Serializer
    permission_classes = [IsAuthenticated, IsElderlyOrFamilyMember]

    def perform_destroy(self, instance):
        """Ensure only the immunization owner or their approved family members can delete."""
        user = self.request.user

        family_member_ids = FamilyMember.objects.filter(
            family_member=user
        ).values_list("user_id", flat=True)

        if instance.user.id not in [user.id, *family_member_ids]:
            raise PermissionDenied("You do not have permission to delete this immunization.")

        instance.delete()


#Blood tests 
class List_BloodTest(generics.ListAPIView):
    queryset=BloodTest.objects.all()
    serializer_class=BloodTest_Serializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        family_member_ids=FamilyMember.objects.filter(family_member=user).values_list("user_id", flat=True)
        return BloodTest.objects.filter(user__in=[user.id, *family_member_ids]).distinct().prefetch_related("user")


class BloodTestDetailView(generics.RetrieveAPIView):
    queryset = BloodTest.objects.all()
    serializer_class = BloodTest_Serializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        """Retrieve a medication only if it belongs to the user or their elderly family members."""
        BloodTest = super().get_object()  # Get the requested BloodTest
        user = self.request.user

        # Get IDs of elderly family members where the user is an approved family member
        family_member_ids = FamilyMember.objects.filter(
            family_member=user
        ).values_list("user_id", flat=True)

        # Check if the BloodTest belongs to the user or their elderly family members
        if BloodTest.user.id not in [user.id, *family_member_ids]:
            raise PermissionDenied("You do not have permission to view this BloodTest.")

        return BloodTest

# Add medication (Elderly user or their family members can add)
class BloodTestCreateView(generics.CreateAPIView):
    queryset = BloodTest.objects.all()
    serializer_class = BloodTest_Serializer
    permission_classes = [IsAuthenticated, IsElderlyOrFamilyMember]

    def perform_create(self, serializer):
        """Assign the logged-in user or their family member as the owner of the medication"""
        serializer.save(user=self.request.user)

# Update medication (Only elderly user or family members can modify)
class BloodTestUpdateView(generics.UpdateAPIView):
    queryset = BloodTest.objects.all()
    serializer_class = BloodTest_Serializer
    permission_classes = [IsAuthenticated, IsElderlyOrFamilyMember]

# Delete medication (Only elderly user or family members can delete)
class BloodTestDeleteView(generics.DestroyAPIView):
    queryset = BloodTest.objects.all()
    serializer_class = BloodTest_Serializer
    permission_classes = [IsAuthenticated, IsElderlyOrFamilyMember]

# 📌 List Diseases (For the user and their elderly family members)
class ListDiseaseView(generics.ListAPIView):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve diseases belonging to the user or their elderly family members."""
        user = self.request.user
        family_member_ids = FamilyMember.objects.filter(
            family_member=user
        ).values_list("user_id", flat=True)

        return Disease.objects.filter(user__in=[user.id, *family_member_ids]).distinct().prefetch_related("user")


# 📌 Retrieve a Specific Disease
class DiseaseDetailView(generics.RetrieveAPIView):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    permission_classes = [IsAuthenticated, IsElderlyOrFamilyMember]

    def get_object(self):
        """Retrieve a disease only if it belongs to the user or their elderly family members."""
        disease = super().get_object()
        user = self.request.user

        family_member_ids = FamilyMember.objects.filter(
            family_member=user
        ).values_list("user_id", flat=True)

        if disease.user.id not in [user.id, *family_member_ids]:
            raise PermissionDenied("You do not have permission to view this disease.")

        return disease


# 📌 Add Disease (Elderly User or Family Member)
class DiseaseCreateView(generics.CreateAPIView):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    permission_classes = [IsAuthenticated, IsElderlyOrFamilyMember]

    def perform_create(self, serializer):
        """Allow a user to add disease records for themselves or an elderly family member."""
        elderly_user_id = self.request.data.get("elderly_user_id")

        if elderly_user_id:
            try:
                elderly_user = Account.objects.get(id=elderly_user_id)
            except Account.DoesNotExist:
                raise ValidationError({"error": "Elderly user not found."})

            is_family_member = FamilyMember.objects.filter(
                user=elderly_user, family_member=self.request.user
            ).exists()

            if not is_family_member and elderly_user != self.request.user:
                raise PermissionDenied("You do not have permission to add disease records for this user.")

            serializer.save(user=elderly_user)
        else:
            serializer.save(user=self.request.user)


# 📌 Update Disease (Only Elderly User or Family Members)
class DiseaseUpdateView(generics.UpdateAPIView):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    permission_classes = [IsAuthenticated, IsElderlyOrFamilyMember]

    def perform_update(self, serializer):
        """Ensure only the disease owner or their approved family members can update."""
        disease = self.get_object()
        elderly_user_id = self.request.data.get("elderly_user_id")

        is_family_member = FamilyMember.objects.filter(
            user=disease.user, family_member=self.request.user
        ).exists()

        if not is_family_member and disease.user != self.request.user:
            raise PermissionDenied("You do not have permission to update this disease record.")

        if elderly_user_id:
            try:
                elderly_user = Account.objects.get(id=elderly_user_id)
            except Account.DoesNotExist:
                raise ValidationError({"error": "Elderly user not found."})

            if not FamilyMember.objects.filter(user=elderly_user, family_member=self.request.user).exists():
                raise PermissionDenied("You do not have permission to update disease records for this user.")

            serializer.save(user=disease.user)  # Keep ownership unchanged
        else:
            serializer.save()


# 📌 Delete Disease (Only Elderly User or Family Members)
class DiseaseDeleteView(generics.DestroyAPIView):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    permission_classes = [IsAuthenticated, IsElderlyOrFamilyMember]

    def perform_destroy(self, instance):
        """Ensure only the disease owner or their approved family members can delete."""
        user = self.request.user

        family_member_ids = FamilyMember.objects.filter(
            family_member=user
        ).values_list("user_id", flat=True)

        if instance.user.id not in [user.id, *family_member_ids]:
            raise PermissionDenied("You do not have permission to delete this disease record.")

        instance.delete()




class ListMRIRecordView(generics.ListAPIView):
    queryset = MRIRecord.objects.all()
    serializer_class = MRIRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve diseases belonging to the user or their elderly family members."""
        user = self.request.user
        family_member_ids = FamilyMember.objects.filter(
            family_member=user
        ).values_list("user_id", flat=True)

        return MRIRecord.objects.filter(user__in=[user.id, *family_member_ids]).distinct().prefetch_related("user")




# 📌 List MRI Records for the User and Their Elderly Family Members
class ListMRIRecordView(generics.ListAPIView):
    queryset = MRIRecord.objects.all()
    serializer_class = MRIRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve MRI records belonging to the user or their elderly family members."""
        user = self.request.user
        family_member_ids = FamilyMember.objects.filter(
            family_member=user
        ).values_list("user_id", flat=True)

        return MRIRecord.objects.filter(user__in=[user.id, *family_member_ids]).distinct().prefetch_related("user")


# 📌 Retrieve a Specific MRI Record
class MRIRecordDetailView(generics.RetrieveAPIView):
    queryset = MRIRecord.objects.all()
    serializer_class = MRIRecordSerializer
    permission_classes = [IsAuthenticated, IsElderlyOrFamilyMember]

    def get_object(self):
        """Retrieve an MRI record only if it belongs to the user or their elderly family members."""
        mri_record = super().get_object()
        user = self.request.user

        family_member_ids = FamilyMember.objects.filter(
            family_member=user
        ).values_list("user_id", flat=True)

        if mri_record.user.id not in [user.id, *family_member_ids]:
            raise PermissionDenied("You do not have permission to view this MRI record.")

        return mri_record


# 📌 Add MRI Record (Elderly User or Family Member)
class MRIRecordCreateView(generics.CreateAPIView):
    queryset = MRIRecord.objects.all()
    serializer_class = MRIRecordSerializer
    permission_classes = [IsAuthenticated, IsElderlyOrFamilyMember]

    def perform_create(self, serializer):
        """Allow a user to add MRI records for themselves or an elderly family member."""
        elderly_user_id = self.request.data.get("elderly_user_id")

        if elderly_user_id:
            elderly_user = get_object_or_404(Account, id=elderly_user_id)
            is_family_member = FamilyMember.objects.filter(
                user=elderly_user, family_member=self.request.user
            ).exists()

            if not is_family_member and elderly_user != self.request.user:
                raise PermissionDenied("You do not have permission to add MRI records for this user.")

            serializer.save(user=elderly_user)
        else:
            serializer.save(user=self.request.user)


# 📌 Update MRI Record (Only Elderly User or Family Members)
class MRIRecordUpdateView(generics.UpdateAPIView):
    queryset = MRIRecord.objects.all()
    serializer_class = MRIRecordSerializer
    permission_classes = [IsAuthenticated, IsElderlyOrFamilyMember]

    def perform_update(self, serializer):
        """Ensure only the MRI record owner or their approved family members can update it."""
        mri_record = self.get_object()
        user = self.request.user

        is_family_member = FamilyMember.objects.filter(
            user=mri_record.user, family_member=user
        ).exists()

        if not is_family_member and mri_record.user != user:
            raise PermissionDenied("You do not have permission to update this MRI record.")

        serializer.save()


# 📌 Delete MRI Record (Only Elderly User or Family Members)
class MRIRecordDeleteView(generics.DestroyAPIView):
    queryset = MRIRecord.objects.all()
    serializer_class = MRIRecordSerializer
    permission_classes = [IsAuthenticated, IsElderlyOrFamilyMember]

    def perform_destroy(self, instance):
        """Ensure only the MRI record owner or their approved family members can delete it."""
        user = self.request.user
        family_member_ids = FamilyMember.objects.filter(
            family_member=user
        ).values_list("user_id", flat=True)

        if instance.user.id not in [user.id, *family_member_ids]:
            raise PermissionDenied("You do not have permission to delete this MRI record.")

        instance.delete()
