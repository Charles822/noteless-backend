from rest_framework import serializers
from .models import Comment, Vote
from notes.models import Note
from django.contrib.auth.models import User
from django.db.models import Sum
from users.serializers import UserSerializer


class CommentCreationSerializer(serializers.Serializer):
    note = serializers.IntegerField(required=True)
    text = serializers.CharField(required=True)
    owner = serializers.IntegerField(required=True)

    def create(self, validated_data):
        text = validated_data['text']
        note_id = validated_data['note']
        owner_id = validated_data['owner']
        note = Note.objects.get(id=note_id)
        owner = User.objects.get(id=owner_id)
        
        comment_instance = Comment.objects.create(
            note=note,
            text=text,
            owner=owner
        )
        
        return comment_instance

class GetCommentsSerializer(serializers.Serializer):
    note = serializers.IntegerField(required=True)

    def get_comments(self, validated_data):
        note_id = validated_data['note']
        comments = Comment.objects.filter(note=note_id)
        
        return comments

class GetCommentsCountSerializer(serializers.Serializer):
    note = serializers.IntegerField(required=True)

    def get_comments_count(self, validated_data):
        note_id = validated_data['note']

        total_count = Comment.objects.filter(note=note_id).count()
                
        return total_count or 0


class CommentSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    updated_at = serializers.SerializerMethodField(
        method_name='get_formatted_date')

    class Meta:
        model = Comment
        fields = ['id', 'note', 'text', 'owner', 'created_at', 'updated_at']

    # Provide a more simple date information for the front end
    def get_formatted_date(self, comment: Comment):
        return comment.updated_at.strftime('%Y-%m-%d')


class VoteCreationSerializer(serializers.Serializer):
    note = serializers.IntegerField(required=True)
    vote = serializers.IntegerField(required=True)
    owner = serializers.IntegerField(required=True)

    def create(self, validated_data):
        vote = validated_data['vote']
        note_id = validated_data['note']
        owner_id = validated_data['owner']
        note = Note.objects.get(id=note_id)
        owner = User.objects.get(id=owner_id)
        
        vote_instance = Vote.objects.create(
            note=note,
            vote=vote,
            owner=owner
        )
        
        return vote_instance

class GetVoteSerializer(serializers.Serializer):
    note = serializers.IntegerField(required=True)
    owner = serializers.IntegerField(required=True)

    def get_vote(self, validated_data):
        note_id = validated_data['note']
        user_id = validated_data['owner']

        vote = Vote.objects.filter(note=note_id, owner=user_id).first()
        
        return vote

class GetVoteSumSerializer(serializers.Serializer):
    note = serializers.IntegerField(required=True)

    def get_votes_sum(self, validated_data):
        note_id = validated_data['note']

        total_sum = Vote.objects.filter(note=note_id).aggregate(total=Sum('vote'))['total']
                
        return max(total_sum or 0, 0)
        

class PatchVoteSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    vote = serializers.IntegerField(required=True)

    def patch_vote(self, validated_data):
        vote_id = validated_data['id']
        new_vote_value = validated_data['vote']

        vote = Vote.objects.filter(id=vote_id).first()

        if vote:
            vote.vote = new_vote_value
            vote.save()
            return vote
        
        return None


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ['id', 'note', 'vote', 'owner', 'created_at', 'updated_at']