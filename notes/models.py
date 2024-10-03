from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid

class Note(models.Model):
    video = models.ForeignKey('contents.Video', on_delete=models.CASCADE)
    response = models.OneToOneField('ai_agent.AgentResponse', on_delete=models.CASCADE)
    note_list = models.ForeignKey('lists.List', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=60, blank=True)
    meta_description = models.TextField(max_length=160, blank=True)

    def __str__(self):
        return f"Note for Video title: {self.video.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.video.title)[:50]  # Truncate to allow space for ID
            unique_id = str(uuid.uuid4())[:8]  # Short UUID
            self.slug = f"{base_slug}-{unique_id}"
        if not self.meta_description:
            self.meta_description = self.response.agent_response[:150]
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'notes'
        ordering = ['-created_at']
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'
