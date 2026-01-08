from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

    
class User(AbstractUser):
    role = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    userDetails_emp = models.JSONField(blank=True, null=True)
    userDetails_job_seeker = models.JSONField(blank=True, null=True)
    userDetails_supervisory = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    deleted_at = models.DateTimeField(null=True, blank=True)
 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()
        
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    class Meta:
        pass