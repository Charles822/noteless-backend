from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django.conf import settings
from .models import List
from .serializers import ListSerializer, ListCreationSerializer
from core.permissions import AdminOnly, IsOwnerOrAdmin

def get_permissions_based_on_action(action):
    # No permission required for retrieving a resource
    if action in ['retrieve', 'list']:
        return [AllowAny]
    elif action == 'add_list':
        return [IsAuthenticated]

    # For other actions, only allow the owner or an admin
    else:
        return [IsOwnerOrAdmin]


class ListViewSet(ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    lookup_field = 'slug'  # Use 'slug' for lookup

    def get_permissions(self):
        return [permission() for permission in get_permissions_based_on_action(self.action)]

    @action(detail=False, methods=['post'], url_path='add_list')
    def add_agent(self, request):
        serializer = ListCreationSerializer(data=request.data)
        
        if serializer.is_valid():
            list_instance = serializer.save()
            response_serializer = ListSerializer(list_instance)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
