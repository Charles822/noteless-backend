from django.db import models


class AgentRole(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Agent Role: {self.name or self.description[:50]}..."
    
    class Meta:
        app_label = 'ai_agent'
        verbose_name = 'Agent Role'
        verbose_name_plural = 'Agent Roles'
        ordering = ['name']


class AgentResponse(models.Model):
    video = models.ForeignKey('contents.Video', on_delete=models.CASCADE)
    transcript = models.ForeignKey('contents.Transcript', on_delete=models.CASCADE)
    agent_role = models.ForeignKey(AgentRole, on_delete=models.CASCADE, related_name='agent_responses')
    agent_response = models.TextField()
    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Response for Video ID {self.video.video_id}"

    class Meta:
        app_label = 'ai_agent'
        verbose_name = 'AgentResponse'
        verbose_name_plural = 'AgentResponses'
        ordering = ['-created_at']