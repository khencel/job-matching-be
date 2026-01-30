from django.db import models
from django.conf import settings

# Create your models here.
class BaseModel(models.Model):
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted = True
        self.save()
        
class JobPost(BaseModel):  
    user_id         = models.IntegerField(null=True)
    title           = models.CharField(max_length=255)
    salary          = models.PositiveIntegerField()
    type_of_emp     = models.JSONField()
    category        = models.JSONField()
    skill           = models.JSONField()
    job_desc        = models.TextField()
    responsibility  = models.TextField()
    who_you_are     = models.TextField()
    nice_to_have    = models.TextField()
    benefits        = models.JSONField(default=list, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "job_post"
        ordering = ['-created_at']
        verbose_name = "Job Post"
        verbose_name_plural = "Job Posts"
    
    def __str__(self):
        return self.title
    