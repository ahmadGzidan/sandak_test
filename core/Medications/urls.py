from django.urls import path
from .views import (
    ListMedicationsView,
    MedicationsDetailView,
    MedicationsCreateView,
    MedicationsUpdateView,
    MedicationsDeleteView,
)

urlpatterns = [
    path("medications/", ListMedicationsView.as_view(), name="medications-list"),
    path("medications/<int:pk>/", MedicationsDetailView.as_view(), name="medications-detail"),
    path("medications/add/", MedicationsCreateView.as_view(), name="medications-create"),
    path("medications/<int:pk>/update/", MedicationsUpdateView.as_view(), name="medications-update"),
    path("medications/<int:pk>/delete/", MedicationsDeleteView.as_view(), name="medications-delete"),
]
