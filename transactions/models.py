from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal
from encrypted_model_fields.fields import EncryptedCharField, EncryptedDateField
from django.utils import timezone

class Category(models.Model):
    CATEGORY_TYPES = (
        ('expense', 'Expense'),
        ('income', 'Income'),
    )
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=7, choices=CATEGORY_TYPES)

    def __str__(self):
        return f"{self.name}"


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('expense', 'Expense'),
        ('income', 'Income'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    amount = EncryptedCharField(max_length=50, default='0.00')  # store amount as encrypted string
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    date = EncryptedDateField()
    description = EncryptedCharField(max_length=255, blank=True)

    def clean(self):
        # Convert amount string to Decimal for validation
        if Decimal(self.amount) <= 0:
            raise ValidationError({'amount': 'Amount must be a positive value.'})

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = timezone.now().date()
        super().save(*args, **kwargs)

    def __str__(self):
        sign = '+'
        if self.type == 'expense':
            sign = '-'

        # Format nicely
        return f"{self.type.capitalize()} - {self.category.name} - {sign}${self.amount}"

