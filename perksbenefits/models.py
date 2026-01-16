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
        
class PerksBenefits(BaseModel):  
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perks_benefits"
    )
    name            = models.CharField(max_length=255)
    description     = models.TextField()
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "perks_benefits"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    