# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class AlumniUser(AbstractUser):
    # --- NEW FIELDS TO ADD ---
    USER_TYPE_CHOICES = (
        ('Student', 'Student'),
        ('Alumni', 'Alumni'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='Alumni')
    # --- END OF NEW FIELDS ---

    # (Keep your existing fields)
    username = None
    email = models.EmailField(unique=True, help_text="College Email Address")
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True)
    batch_year = models.IntegerField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'batch_year']

    def __str__(self):
        return self.full_name