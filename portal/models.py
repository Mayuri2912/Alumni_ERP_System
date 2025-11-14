# portal/models.py
from django.db import models
from django.conf import settings

class Post(models.Model):
    POST_TYPES = (
        ('General', 'General'),
        ('Hiring', 'Hiring'), # For Jobs & Referrals
        ('Meetup', 'Meetup'),
        ('Invite', 'Invite'),
        ('Announcement', 'Announcement'), 
    )

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default='General')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Optional fields for Meetups
    meetup_time = models.DateTimeField(null=True, blank=True)
    meetup_location = models.CharField(max_length=255, null=True, blank=True)

    # --- !! THIS IS THE NEW FIELD FOR MODERATION !! ---
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.full_name}: {self.content[:30]}..."