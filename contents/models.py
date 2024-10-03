from django.db import models


class Video(models.Model):
    youtube_url = models.URLField(max_length=255)
    youtube_video_id = models.CharField(max_length=50)
    title = models.CharField(max_length=255, blank=True, null=True)
    channel_name = models.CharField(max_length=255)
    original_language = models.CharField(max_length=50, null=True)
    duration = models.CharField(max_length=20, null=True)
    tags = models.JSONField(null=True, blank=True)
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or self.video_id

    class Meta:
    	app_label = 'contents'


class Transcript(models.Model):
    transcript_text = models.JSONField(null=True, blank=True)
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name='transcripts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Transcript for {self.video.title or self.video.video_id}'

    class Meta:
    	app_label = 'contents'