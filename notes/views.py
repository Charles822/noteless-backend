from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Note
from lists.models import List
from .serializers import NoteSerializer, NoteCreationSerializer
from htfbi_backend.tasks import create_note_task 
from core.permissions import AdminOnly, IsListOwnerOrAdmin
from celery.result import AsyncResult

def get_permissions_based_on_action(action):
    # No permission required for retrieving a resource
    if action in ['retrieve', 'list', 'check_task_status']:
        return [AllowAny]

    elif action == 'add_note':
        print('He is owner or admin')
        return [IsListOwnerOrAdmin]
        
    # For other actions, only allow the owner or an admin
    else:
        return [AdminOnly]

class NoteViewSet(ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'  # Use 'slug' for lookup

    def get_permissions(self):
        return [permission() for permission in get_permissions_based_on_action(self.action)]

    def get_queryset(self):
        list_slug = self.kwargs.get('list_slug')
        queryset = Note.objects.annotate(
            votes_count=Sum('votes__vote')
        ).order_by('-votes_count', '-created_at')
        
        if list_slug is not None:
            list_instance = get_object_or_404(List, slug=list_slug)
            return queryset.filter(note_list=list_instance)
        return queryset


    @action(detail=False, methods=['post'], url_path='add_note')
    def add_note(self, request, *args, **kwargs):
        note_data = request.data
        task_result = create_note_task.delay(note_data)
        
        # Respond immediately that the task is in progress
        return Response({
            "message": "Note creation is in progress.",
            "taskId": task_result.id
            }, status=status.HTTP_202_ACCEPTED)


    @action(detail=False, methods=['get'], url_path='check_task_status/(?P<task_id>[^/.]+)')
    def check_task_status(self, request, task_id=None):
        task_result = AsyncResult(task_id)
        if task_result.successful():
            return Response({'status': 'SUCCESS', 'note_id': task_result.result['note_id']})
        elif task_result.failed():
            return Response({'status': 'FAILURE'})
        else:
            return Response({'status': 'PENDING'})
