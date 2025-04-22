from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Transportation', 'Transportation'),
        ('Entertainment', 'Entertainment'),
        ('Rent', 'Rent'),
        ('Savings', 'Savings'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=255, blank=True)
    income = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.category} - ${self.amount}"
