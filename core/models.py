from django.db import models
from django.contrib.auth.models import AbstractUser

class OpsUser(AbstractUser):
    is_ops_user = models.BooleanField(default=True)

class ClientUser(AbstractUser):
    is_client_user = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

class File(models.Model):
    ops_user = models.ForeignKey(OpsUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
