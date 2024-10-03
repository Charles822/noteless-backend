from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import AgentRole, AgentResponse
from .serializers import AgentRoleSerializer, AgentResponseSerializer
from core.permissions import AdminOnly

def get_permissions_based_on_action(action):
    # No permission required for retrieving a resource
    if action == 'retrieve':
        return [AllowAny]
        
    # For other actions, only allow the owner or an admin
    else:
        return [AdminOnly]


class AgentRoleViewSet(ModelViewSet):
    queryset = AgentRole.objects.all()
    serializer_class = AgentRoleSerializer

    def get_permissions(self):
        return [permission() for permission in get_permissions_based_on_action(self.action)]


class AgentResponseViewSet(ModelViewSet):
    queryset = AgentResponse.objects.all()
    serializer_class = AgentResponseSerializer

    def get_permissions(self):
        return [permission() for permission in get_permissions_based_on_action(self.action)]