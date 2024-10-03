from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Customer(models.Model):
    MEMBERSHIP_FREE = 'F'
    MEMBERSHIP_CONTRIBUTOR = 'C'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_FREE, 'Free'),
        (MEMBERSHIP_CONTRIBUTOR, 'Contributor'),
    ]
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_FREE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.first_name or ""} {self.user.last_name or ""}'.strip()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.user.username