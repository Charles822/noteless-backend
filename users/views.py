from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.conf import settings
from .models import Customer, Profile
from .serializers import UserSerializer, ProfileSerializer, CustomerSerializer, MyTokenObtainPairSerializer, UserCreationSerializer
from core.permissions import AdminOnly, IsOwnerOrAdmin


def get_permissions_based_on_action(action):
    # No permission required to create a user
    if action == 'create':
        return [AllowAny]
    # For other actions, only allow the owner or an admin
    else:
        return [IsOwnerOrAdmin]


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        return [permission() for permission in get_permissions_based_on_action(self.action)]

    @action(detail=False, methods=['post'], url_path='create_user')
    def add_agent(self, request):
        serializer = UserCreationSerializer(data=request.data)
        
        if serializer.is_valid():
            new_user = serializer.save()
            response_serializer = UserSerializer(new_user)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='my-profile')
    def get_profile(self, request):
        profile = request.user.profile
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer