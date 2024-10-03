from django.db.models import Sum
from django.contrib.auth.models import User
from datetime import datetime
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .models import Note
from ai_agent.models import AgentResponse, AgentRole
from ai_agent.llama3_agent import get_agent_response
from ai_agent.serializers import AgentResponseSerializer
from contents.models import Video, Transcript
from contents.youtube_data import fetch_video_info, fetch_video_transcript, extract_video_id
from contents.serializers import VideoSerializer
from lists.models import List
from users.serializers import UserSerializer

class NoteCreationSerializer(serializers.Serializer):
    youtube_url = serializers.URLField(required=True)
    note_list = serializers.IntegerField(required=True)
    owner = serializers.IntegerField(required=True)

    def create(self, validated_data):
        youtube_url = validated_data['youtube_url']
        list_id = validated_data['note_list']
        owner_id = validated_data['owner']

        # check if a note associated to this video already exists in the list before going further
        video = Video.objects.filter(youtube_url=youtube_url)
        if video.exists():
            video_instance=video.get()
        
            if Note.objects.filter(video=video_instance).exists():
                raise ValidationError({"error": "A note for this content already exists in this list."})

        # get the youtube video ID
        youtube_video_id = extract_video_id(youtube_url)

        # Create or retrieve the video instance
        def get_video_instance(youtube_video_id):
            # check if the video instance already exists
            existing_video_instance = Video.objects.filter(youtube_video_id=youtube_video_id)
            if existing_video_instance:
                return existing_video_instance.get()

            # if not, create a new one
            video_data = fetch_video_info(youtube_video_id)

            if 'items' not in video_data or not video_data['items']:
                return Response({"error": "Invalid video ID or no data found"}, status=status.HTTP_404_NOT_FOUND)

            # Extract the relevant data
            video_info = video_data['items'][0]['snippet']
            content_detail = video_data['items'][0]['contentDetails']

            #Verify that default language is provided
            def is_original_language_provided(): 
                if 'defaultAudioLanguage' in video_info:
                    return video_info['defaultAudioLanguage']
                return 'na'

            original_language = is_original_language_provided()

            new_video_instance = Video.objects.create(
                youtube_video_id=youtube_video_id,
                title=video_info['title'],
                channel_name=video_info['channelTitle'],
                youtube_url=youtube_url,
                published_at=video_info['publishedAt'],
                duration=content_detail['duration'],
                tags=video_info.get('tags', []),
                original_language=original_language
            )
            
            return new_video_instance

        video_instance = get_video_instance(youtube_video_id)

        # Check if the video exists
        try:
            video_instance
        except video_instance.DoesNotExist:
            return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)


        # get or create transcript instance
        def get_transcript_instance(video_instance):
            # Check if the transcript instance exists 
            existing_transcript = Transcript.objects.filter(video=video_instance.id)
            if existing_transcript:
                return existing_transcript.get()

            # if it doesn't exist, create a new transcript 
            video_transcript = fetch_video_transcript(video_instance.id)

            if video_transcript is None: #catch error
                return Response({"error": "Transcript not found or error fetching transcript"}, status=status.HTTP_404_NOT_FOUND)

            new_transcript_instance = Transcript.objects.create(
                transcript_text=video_transcript,
                video=video_instance,
            )

            return new_transcript_instance

        transcript_instance = get_transcript_instance(video_instance)

        # Create the AgentResponse instance
        
        # get agent_id via the List
        list_id = list_id
        owner_id = owner_id
        list_instance = List.objects.get(id=list_id)
        agent_id = list_instance.agent_role_id
        agent_role = AgentRole.objects.get(id=agent_id)
        owner = User.objects.get(id=owner_id)
        
        # generate response with the agent
        agent_response = get_agent_response(transcript_instance.transcript_text, agent_role.description)
        agent_response_instance = AgentResponse.objects.create(
            video=video_instance,
            transcript=transcript_instance,
            agent_role=agent_role,
            agent_response=agent_response,
        )
        
        # Create the Note instance
        note_instance = Note.objects.create(
            video=video_instance,
            response=agent_response_instance,
            note_list=list_instance,
            owner=owner,
            )

        return note_instance


class NoteSerializer(serializers.ModelSerializer):
    video = VideoSerializer(read_only=True)
    owner = UserSerializer(read_only=True)
    response = AgentResponseSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField(
        method_name='get_comments_count')
    votes_count = serializers.SerializerMethodField(
        method_name='get_votes_sum')
    created_at = serializers.SerializerMethodField(
        method_name='get_formatted_date')

    class Meta:
        model = Note
        fields = ['id', 'video', 'response', 'note_list', 'owner', 'comments_count', 'votes_count', 'created_at', 'slug', 'meta_description']


    def get_comments_count(self, note: Note):
        return note.comments.count()

    def get_votes_sum(self, note: Note):
        total_sum = note.votes.aggregate(total=Sum('vote'))['total'] or 0
        return max(total_sum, 0)

    # Provide a more simple date information for the front end
    def get_formatted_date(self, note: Note):
        if isinstance(note.created_at, str):
            # Parse the date string into a datetime object
            note.created_at = datetime.fromisoformat(note.created_at)
            return note.created_at.strftime('%Y-%m-%d')
        return note.created_at.strftime('%Y-%m-%d')




