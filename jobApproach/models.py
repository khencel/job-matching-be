from django.db import models


# Create your models here.
class BaseModel(models.Model):
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted = True
        self.save()
        
class JobApproach(BaseModel):  
    data            = models.JSONField()
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "job_approach"
        ordering = ['-created_at']
    
    