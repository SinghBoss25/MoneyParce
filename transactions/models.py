from django.db import models
from django.conf import settings

CATEGORY_CHOICES = [
    ('food', 'Food'),
    ('transport', 'Transportation'),
    ('entertainment', 'Entertainment'),
    ('utilities', 'Utilities'),
    ('other', 'Other'),
]

class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - ${self.amount}"
