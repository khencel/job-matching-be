from django.db import models
from userauth.models import User
import os
from django.db.models.signals import pre_save
from django.dispatch import receiver


def upload_document_path(instance, filename):
    return os.path.join(
        'document',
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
        
class ApplicantDocument(BaseModel):  
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    documents = models.FileField(upload_to=upload_document_path, blank=True, null=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "applicant_document"
        ordering = ['-created_at']
        verbose_name = "Job Seeker Document"
        verbose_name_plural = "Job Seeker Document"
        

