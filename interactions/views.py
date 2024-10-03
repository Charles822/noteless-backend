from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django.conf import settings
from .models import Comment, Vote
from .serializers import CommentSerializer, CommentCreationSerializer, VoteSerializer, VoteCreationSerializer, GetVoteSerializer, PatchVoteSerializer, GetVoteSumSerializer, GetCommentsCountSerializer, GetCommentsSerializer
from core.permissions import IsOwnerOrAdmin


def get_permissions_based_on_action(action):
    # No permission required for retrieving a resource
    if action == ['retrieve', 'list']:
        return [AllowAny]
    # Allow any authenticated user to create a resource
    elif action == 'create':
        return [IsAuthenticated]
    # For other actions, only allow the owner or an admin
    else:
        return [IsOwnerOrAdmin]


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_permissions(self):
        return [permission() for permission in get_permissions_based_on_action(self.action)]

    def get_queryset(self):
        note_id = self.kwargs.get('note_pk')
        if note_id is not None:
            return Comment.objects.filter(note=note_id)
        return Comment.objects.all()

    @action(detail=False, methods=['post'], url_path='add_comment')
    def add_comment(self, request, *args, **kwargs):
        serializer = CommentCreationSerializer(data=request.data)
        
        if serializer.is_valid():
            comment_instance = serializer.save()
            response_serializer = CommentSerializer(comment_instance)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='note_comments')
    def note_comments(self, request, *args, **kwargs):
        serializer = GetCommentsSerializer(data=request.query_params)

        if serializer.is_valid():
            comments = serializer.get_comments(serializer.validated_data)
            
            if comments.exists():
                comments_data = CommentSerializer(comments, many=True).data
                return Response({'have_comments': True, 'comments': comments_data}, status=status.HTTP_200_OK)
        
        return Response({'no_comments': False}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='comments_count')
    def comments_count(self, request, *args, **kwargs):
        serializer = GetCommentsCountSerializer(data=request.query_params)

        if serializer.is_valid():
            comments_count = serializer.get_comments_count(serializer.validated_data)
            return Response({'comments_count': comments_count}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class VoteViewSet(ModelViewSet):
    serializer_class = VoteSerializer

    def get_permissions(self):
        return [permission() for permission in get_permissions_based_on_action(self.action)]

    def get_queryset(self):
        note_id = self.kwargs.get('note_pk')
        if note_id is not None:
            return Vote.objects.filter(note=note_id)
        return Vote.objects.all()

    @action(detail=False, methods=['post'], url_path='add_vote')
    def add_vote(self, request, *args, **kwargs):
        serializer = VoteCreationSerializer(data=request.data)
        
        if serializer.is_valid():
            vote_instance = serializer.save()
            response_serializer = VoteSerializer(vote_instance)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='user_vote')
    def user_vote(self, request, *args, **kwargs):
        serializer = GetVoteSerializer(data=request.query_params)

        if serializer.is_valid():
            vote = serializer.get_vote(serializer.validated_data)
            if vote:
                return Response({'has_voted': True, 'vote': VoteSerializer(vote).data}, status=status.HTTP_200_OK)
        
        return Response({'has_voted': False}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='votes_sum')
    def votes_sum(self, request, *args, **kwargs):
        serializer = GetVoteSumSerializer(data=request.query_params)

        if serializer.is_valid():
            votes_sum = serializer.get_votes_sum(serializer.validated_data)
            return Response({'votes_sum': votes_sum}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['patch'], url_path='patch_vote')
    def patch_vote(self, request, *args, **kwargs):
        serializer = PatchVoteSerializer(data=request.data)

        if serializer.is_valid():
            new_vote = serializer.patch_vote(serializer.validated_data)
            if new_vote:
                return Response({'has_updated_vote': True, 'vote': VoteSerializer(new_vote).data}, status=status.HTTP_200_OK)
            
        return Response({'has_updated_voted': False}, status=status.HTTP_400_BAD_REQUEST)


