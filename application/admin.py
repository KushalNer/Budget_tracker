from django.contrib import admin
from .models import user, Category, Income, Expense,Transaction, Reminder
# Register your models here.
admin.site.register(user)
admin.site.register(Category)
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(Transaction)
admin.site.register(Reminder)