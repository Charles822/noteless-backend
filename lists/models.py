from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class List(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    agent_role = models.ForeignKey('ai_agent.AgentRole', on_delete=models.CASCADE)
    is_closed = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    meta_description = models.TextField(max_length=160, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:60]
        if not self.meta_description:
            self.meta_description = self.description[:150]
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'lists'
        ordering = ['-created_at']
        verbose_name = 'List'
        verbose_name_plural = 'Lists'



