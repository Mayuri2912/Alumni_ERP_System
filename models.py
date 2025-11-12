from django.db import models
# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class AlumniUser(AbstractUser):
    # We want to use email as the primary login field
    username = None
    email = models.EmailField(unique=True, help_text="College Email Address")
    
    # Additional fields from your sign-up form
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True)
    batch_year = models.IntegerField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'batch_year']

    def __str__(self):
        return self.full_name
