from django.contrib import admin
from .models import Account
from .models import FamilyMember

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'gender', 'is_active', 'is_staff','personal_image','date_of_birth')


@admin.register(FamilyMember)
class familyMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'family_member', 'relationship_type')
