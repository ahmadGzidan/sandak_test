from django.urls import path
from .views import (
    # Immunization Views
    List_Immunization, ImmunizationCreateView, ImmunizationDeleteView, 
    ImmunizationDetailView, ImmunizationUpdateView, 

    # Blood Test Views
    List_BloodTest, BloodTestCreateView, BloodTestDeleteView, 
    BloodTestDetailView, BloodTestUpdateView,

    # Disease Views
    ListDiseaseView, DiseaseCreateView, DiseaseDeleteView, 
    DiseaseDetailView, DiseaseUpdateView,
    
    # MRI Record Views
    ListMRIRecordView, MRIRecordCreateView, MRIRecordDeleteView, 
    MRIRecordDetailView, MRIRecordUpdateView
)

urlpatterns = [
    # Immunization
    path("immunizations/", List_Immunization.as_view(), name="list_immunizations"),
    path("immunizations/<int:pk>/", ImmunizationDetailView.as_view(), name="immunization_detail"),
    path("immunizations/add/", ImmunizationCreateView.as_view(), name="immunization_create"),
    path("immunizations/<int:pk>/update/", ImmunizationUpdateView.as_view(), name="immunization_update"),
    path("immunizations/<int:pk>/delete/", ImmunizationDeleteView.as_view(), name="immunization_delete"),

    # Blood Tests
    path("blood-tests/", List_BloodTest.as_view(), name="list_blood_tests"),
    path("blood-tests/<int:pk>/", BloodTestDetailView.as_view(), name="blood_test_detail"),
    path("blood-tests/add/", BloodTestCreateView.as_view(), name="blood_test_create"),
    path("blood-tests/<int:pk>/update/", BloodTestUpdateView.as_view(), name="blood_test_update"),
    path("blood-tests/<int:pk>/delete/", BloodTestDeleteView.as_view(), name="blood_test_delete"),

    # Diseases
    path("diseases/", ListDiseaseView.as_view(), name="list_diseases"),
    path("diseases/<int:pk>/", DiseaseDetailView.as_view(), name="disease_detail"),
    path("diseases/add/", DiseaseCreateView.as_view(), name="disease_create"),
    path("diseases/<int:pk>/update/", DiseaseUpdateView.as_view(), name="disease_update"),
    path("diseases/<int:pk>/delete/", DiseaseDeleteView.as_view(), name="disease_delete"),
    
    # MRI Records
    path("mri-records/", ListMRIRecordView.as_view(), name="list_mri_records"),
    path("mri-records/<int:pk>/", MRIRecordDetailView.as_view(), name="mri_record_detail"),
    path("mri-records/add/", MRIRecordCreateView.as_view(), name="mri_record_create"),
    path("mri-records/<int:pk>/update/", MRIRecordUpdateView.as_view(), name="mri_record_update"),
    path("mri-records/<int:pk>/delete/", MRIRecordDeleteView.as_view(), name="mri_record_delete"),
]
