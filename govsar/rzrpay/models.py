from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from website.models import Item

transaction_status = [
    ("pending","Pending"),
    ("failed","Failed"),
    ("success","Success")
]

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    items = models.ForeignKey(Item, on_delete=models.CASCADE, default=2)
    razorpay_order_id = models.CharField(max_length=256)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    amount = models.FloatField()
    status = models.CharField(choices=transaction_status, max_length=7)
    tax = models.FloatField() 
    created = models.DateTimeField(auto_now_add=True)