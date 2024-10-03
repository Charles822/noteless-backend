from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Video, Transcript
from .serializers import VideoSerializer, TranscriptSerializer
from core.permissions import AdminOnly

def get_permissions_based_on_action(action):
    # No permission required for retrieving a resource
    if action == 'retrieve':
        return [AllowAny]
        
    # For other actions, only allow the owner or an admin
    else:
        return [AdminOnly]


class VideoViewSet(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def get_permissions(self):
        return [permission() for permission in get_permissions_based_on_action(self.action)]


class TranscriptViewSet(ModelViewSet):
    queryset = Transcript.objects.all()
    serializer_class = TranscriptSerializer

    def get_permissions(self):
        return [permission() for permission in get_permissions_based_on_action(self.action)]








