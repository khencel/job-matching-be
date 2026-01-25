from django.db import models
from post_a_job.models import JobPost
from userauth.models import User

# Create your models here.
class BaseModel(models.Model):
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted = True
        self.save()
        
class JobApply(BaseModel):  
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    employer_id = models.IntegerField(null=True, blank=True)
    job_post = models.ForeignKey(
        JobPost,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    status = models.CharField(max_length=20, null=True, blank=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "job_apply"
        ordering = ['-created_at']
        verbose_name = "Job Apply"
        verbose_name_plural = "Job Apply"

    def __str__(self):
        return f"Job Apply for Job Post {self.job_post_id}"