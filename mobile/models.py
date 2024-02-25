from django.conf import settings
from django.db import models
import uuid

User = settings.AUTH_USER_MODEL

class APIKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Генерация уникального ключа при сохранении объекта
        if not self.key:
            self.key = str(uuid.uuid4())
        super().save(*args, **kwargs)