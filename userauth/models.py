from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid
import os
from django.db.models.signals import pre_save
from django.dispatch import receiver


def avatar_upload_path(instance, filename):
    return os.path.join('avatar', str(instance.id), filename)

def banner_upload_path(instance, filename):
    return os.path.join('banner', str(instance.id), filename)
    
class User(AbstractUser):
    role = models.CharField(max_length=255, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    userDetails_emp = models.JSONField(blank=True, null=True)
    userDetails_job_seeker = models.JSONField(blank=True, null=True)
    userDetails_supervisory = models.JSONField(blank=True, null=True)
    
    avatar = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True)
    banner = models.ImageField(upload_to=banner_upload_path, blank=True, null=True)
    
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
    
    
@receiver(pre_save, sender=User)
def auto_delete_old_avatar(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old = User.objects.get(pk=instance.pk)
    except User.DoesNotExist:
        return

    if old.avatar and instance.avatar and old.avatar != instance.avatar:
        old.avatar.delete(save=False)
        
@receiver(pre_save, sender=User)
def auto_delete_old_banner(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old = User.objects.get(pk=instance.pk)
    except User.DoesNotExist:
        return

    if old.banner and instance.banner and old.banner != instance.banner:
        old.banner.delete(save=False)
    

    
class EmailVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)