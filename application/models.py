from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
# Create your models here.
class user(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    password = models.CharField(max_length=50)
    register_at = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.name} -- {self.email}"


class Category(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.name

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    #time = models.TimeField(default=timezone.localtime)

    def __str__(self):
        return f"{self.source} - {self.amount}"
    
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    #time = models.TimeField(default=timezone.localtime)

    def __str__(self):
        return f"{self.category} - {self.amount}"
    
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=100, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    time = models.TimeField(default=timezone.localtime)

    def __str__(self):
        return f"{self.type}--{self.user}"
    
class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    time = models.TimeField(default=datetime.now)  # store reminder time
    date = models.DateField(default=datetime.now)  # store reminder date
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.message} - {self.date} {self.time}"