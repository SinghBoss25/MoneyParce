from django.contrib import admin

# Register your models here.
# finance/admin.py


from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'category', 'type', 'amount', 'description')
    list_filter = ('user', 'category', 'type', 'date')
    search_fields = ('user__username', 'category', 'description')

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Transaction

class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 0

class CustomUserAdmin(UserAdmin):
    inlines = [TransactionInline]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
