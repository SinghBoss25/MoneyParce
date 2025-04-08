from django.db import models
from django.conf import settings

class BankConnection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100)
    access_token = models.CharField(max_length=512)  # Encrypted in production!
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.bank_name}"
