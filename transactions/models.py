from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal

class Category(models.Model):
    CATEGORY_TYPES = (
        ('expense', 'Expense'),
        ('income', 'Income'),
    )
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=7, choices=CATEGORY_TYPES)

    def __str__(self):
        return f"{self.name} ({self.type})"


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('expense', 'Expense'),
        ('income', 'Income'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)

    def clean(self):
        # Ensure that amount is positive
        if self.amount <= 0:
            raise ValidationError({'amount': 'Amount must be a positive value.'})

    def __str__(self):
        # Use a single "-" for expenses, and "+" for income
        sign = '+'
        if (self.type == 'expense'):
            sign = '-'

        return f"{self.type.capitalize()} - {self.category.name} - {sign}${self.amount}"




