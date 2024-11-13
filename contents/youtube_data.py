from decouple import config
import googleapiclient.discovery
from youtube_transcript_api import YouTubeTranscriptApi
import json
from contents.models import Video
from urllib.parse import urlparse, parse_qs

def extract_video_id(youtube_url):
    query = urlparse(youtube_url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p.get('v', [None])[0]
        if query.path.startswith('/embed/'):
            return query.path.split('/')[2]
        if query.path.startswith('/v/'):
            return query.path.split('/')[2]
    # fail?
    return None

def fetch_video_info(video_id):
    # Set up the API key and YouTube API client
    api_service_name = "youtube"
    api_version = "v3"
    api_key = config('YT_API_KEY')

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=api_key)

    request = youtube.videos().list(
        part="snippet,contentDetails",
        id=video_id
    )
    response = request.execute()

    return response

# need to handle the logic to fetch the original language

def validate_transcript_language(transcript_list, video_language):
    for transcript in transcript_list:
        if not transcript.is_generated:
            if '-' in video_language:
                return video_language.split('-')[0]
            return video_language
        return transcript.language_code

def fetch_video_transcript(content_id):

    video = Video.objects.filter(id=content_id).get()
    video_yt_id = video.youtube_video_id
    video_language = video.original_language

    # validate available transcript language
    # Use a proxy for transcript API to work in production
    proxy_username = config('PROXY_USERNAME')
    proxy_password = config('PROXY_PASSWORD')
    proxy = { 
        "https": f"https://{proxy_username}:{proxy_password}@gate.visitxiangtan.com:10001"
    }


    #validate the transcript language

    # for prod env
    # transcript_list = YouTubeTranscriptApi.list_transcripts(video_yt_id, proxies=proxy)
    # for dev
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_yt_id)
    
    validated_language = validate_transcript_language(transcript_list, video_language)

    # get transcript with validated languag

    # for prod env
    # transcript = YouTubeTranscriptApi.get_transcript(video_yt_id, languages=[validated_language], proxies=proxy)
    #for dev env
    transcript = YouTubeTranscriptApi.get_transcript(video_yt_id, languages=[validated_language])


    return transcript