from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Extend if needed later (e.g., profile image, notifications, etc.)
    pass
