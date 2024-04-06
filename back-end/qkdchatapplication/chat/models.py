from django.db import models
import uuid

# Create your models here.
class chatMsg(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.CharField(max_length = 100)
    message = models.CharField(max_length = 100)