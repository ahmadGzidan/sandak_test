from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from accounts.serializers import RegistrationSerializer, FamilyMemberSerializer,ProfileSerializer
from .models import Account, FamilyMember
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve the current user's profile."""
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """Update the current user's profile."""
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@permission_classes([IsAuthenticated])
def search_for_a_user(request, username):
    try:
        user = Account.objects.get(username=username)
        return JsonResponse({
            "id": user.id,
            "username": user.username,
        },status=302)
    except Account.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)


@api_view(['POST'])
def registration_view(request):
    parser_classes = (MultiPartParser, FormParser)  # Ensure the view can handle file uploads

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['id'] = account.id
            data['response'] = 'Successfully registered new user.'
            data['email'] = account.email
            data['username'] = account.username
            data['first_name'] = account.first_name
            data['last_name'] = account.last_name
            data['gender'] = account.gender
            data['date_of_birth'] = account.date_of_birth
            data['personal_image'] = request.build_absolute_uri(account.personal_image.url) if account.personal_image else None  # Fix image handling
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors

        return Response(data)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    token = request.auth

    if token:
        token.delete()
        return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'No token provided.'}, status=status.HTTP_400_BAD_REQUEST)

class FamilyMemberViewSet(viewsets.ModelViewSet):
    serializer_class = FamilyMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Only return the logged-in user's family members"""
        return FamilyMember.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Ensure that the logged-in user is set as the owner"""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["delete"], permission_classes=[permissions.IsAuthenticated])
    def remove(self, request, pk=None):
        """Remove a family member"""
        try:
            family_member = FamilyMember.objects.get(id=pk, user=request.user)
            family_member.delete()
            return Response({"message": "Family member removed successfully."}, status=status.HTTP_204_NO_CONTENT)
        except FamilyMember.DoesNotExist:
            return Response({"error": "Family member not found."}, status=status.HTTP_404_NOT_FOUND)
