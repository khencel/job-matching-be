from django.db import models
from userauth.models import User
import os
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.

def upload_resume_path(instance, filename):
    return os.path.join(
        'resume',
        f'user_{instance.user.id}',
        filename
    )

class BaseModel(models.Model):
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted = True
        self.save()
        
class MyResume(BaseModel):  
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    resume_info = models.JSONField()
    resume = models.FileField(upload_to=upload_resume_path, blank=True, null=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "my_resume"
        ordering = ['-created_at']
        verbose_name = "My Resume"
        verbose_name_plural = "My Resumes"
        
        
@receiver(pre_save, sender=MyResume)
def auto_delete_old_resume(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old = MyResume.objects.get(pk=instance.pk)
    except MyResume.DoesNotExist:
        return

    if old.resume and instance.resume and old.resume != instance.resume:
        old.resume.delete(save=False)
