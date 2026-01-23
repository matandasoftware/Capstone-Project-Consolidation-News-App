from django.db import models
from django.conf import settings

# Create your models here.
class ResetToken(models.Model):
    """Model to store password reset tokens."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=500)
    expiry_date = models.DateTimeField()
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Reset token for {self.user.username}"
    
    class Meta:
        ordering = ['-created_at']