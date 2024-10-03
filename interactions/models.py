from django.db import models
from django.contrib.auth.models import User

class Vote(models.Model):
    UPVOTE = 1
    DOWNVOTE = -1
    NEUTRAL = 0

    VOTE_CHOICES = [
        (UPVOTE, 'Upvote'),
        (DOWNVOTE, 'Downvote'),
        (NEUTRAL, 'Neutral'),
    ]

    note = models.ForeignKey('notes.Note', on_delete=models.CASCADE, related_name='votes')
    vote = models.IntegerField(choices=VOTE_CHOICES, default=NEUTRAL)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        vote_type = dict(self.VOTE_CHOICES).get(self.vote, 'Unknown')
        return f"{vote_type} for Note ID {self.note.id}"

    class Meta:
        app_label = 'interactions'
        unique_together = ('owner', 'note')  # Ensure one vote per user per note
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'


class Comment(models.Model):
    note = models.ForeignKey('notes.Note', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f" Comment {self.id} for Note ID {self.note.id}"

    class Meta:
        app_label = 'interactions'
        ordering = ['created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'