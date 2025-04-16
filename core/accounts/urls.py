from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from .views import FamilyMemberViewSet,search_for_a_user,UserProfileView

urlpatterns = [
    # Other URL patterns for the 'accounts' app
    path('registration/', views.registration_view, name='registration'),
    path('login/', obtain_auth_token, name="login"),
    path('logout/', views.logout, name='logout'),

    #search for a userr 
    path('search-for-a-user/<str:username>/', search_for_a_user, name='search_for_a_user'),
    #user profile 
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    #adding family member 
    path("family-members/", FamilyMemberViewSet.as_view({"get": "list", "post": "create"}), name="family-list"),
    path("family-members/<int:pk>/remove/", FamilyMemberViewSet.as_view({"delete": "remove"}), name="family-remove"),
]
