# portal/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Post
from accounts.models import AlumniUser

@receiver(post_save, sender=Post)
def send_job_notification(sender, instance, created, **kwargs):
    # Check if a new post was just created AND its type is 'Hiring'
    if created and instance.post_type == 'Hiring':
        
        student_emails = AlumniUser.objects.all().values_list('email', flat=True)

        subject = f"New Job Referral Posted by {instance.author.full_name}"
        message = f"""
        Hi,
        
        A new job/referral opportunity has been posted on the alumni portal.
        
        Post: "{instance.content}"
        
        Log in to the portal to view more details.
        
        Best,
        MIT-WPU Alumni Team
        """
        
        send_mail(
            subject,
            message,
            'noreply@yourdomain.com', # From email
            list(student_emails),     # List of recipients
            fail_silently=False,
        )