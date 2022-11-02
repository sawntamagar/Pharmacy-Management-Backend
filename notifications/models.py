from django.db import models
from account.models import PmsUser

class Notification(models.Model):
    user = models.ForeignKey(PmsUser, related_name="notifications", on_delete=models.CASCADE)
    body = models.TextField(blank=True, null=True)
    is_seen = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        super(Notification, self).save(*args, **kwargs)
        