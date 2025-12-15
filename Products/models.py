from django.db import models
from userauth.models import User

# Create your models here.
class BaseModel(models.Model):
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted = True
        self.save()
        
        
class Products(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.name} by {self.user.username}"

