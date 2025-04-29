from django.db import models
from django.contrib.auth.models import User
from transactions.models import Transaction, Category
from django.core.mail import send_mail

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField(auto_now_add=True)
    notified = models.BooleanField(default=False)

    def progress(self):
        if self.amount == 0:
            return 0
        total = 0
        transactions = Transaction.objects.filter(
            user=self.user,
            date__year=self.month.year,
            date__month=self.month.month
        )

        for t in transactions:
            if "expense" in t.type.lower() and t.category == self.category:
                total += float(t.amount)
        progress = (total / float(self.amount)) * 100
        if progress >= 90 and not self.notified:
            # Send email
            send_mail(
                subject='MoneyParce Budget Alert!',
                message=f'You have spent {progress:.0f}% of your budget for {self.category.name}!\nYou are approaching your monthly limit so please spend carefully.',
                from_email=None,  # uses DEFAULT_FROM_EMAIL
                recipient_list=[self.user.email],
                fail_silently=False,
            )
            self.notified = True 
            self.save()
        return (total / float(self.amount)) * 100
    
    def total(self):
        if self.amount == 0:
            return 0
        total = 0
        transactions = Transaction.objects.filter(
            user=self.user,
            date__year=self.month.year,
            date__month=self.month.month
        )

        for t in transactions:
            if "expense" in t.type.lower() and t.category == self.category:
                total += float(t.amount)
        return total

    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.month}"

class FinancialGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deadline = models.DateField()

    def progress(self):
        if self.target_amount == 0:
            return 0
        return (self.current_amount / self.target_amount) * 100

    def __str__(self):
        return f"{self.user.username} - {self.name}"