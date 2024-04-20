from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from phonenumber_field.formfields import PhoneNumberField

now = timezone.now() 
  
class Category(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=254)
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    
    class Meta:
        ordering = ('created_at',)
        
    def __str__(self):
        return self.title 
  
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pfp = models.ImageField(upload_to='user_pfp', blank=True, null=True)
    liked_posts = models.ManyToManyField(Post, related_name='liked_by_users', blank=True)
    phone = models.CharField(max_length=15, default='1234567890')
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username

    
sizes = [
    ("small","Small"),
    ("medium","Medium"),
    ("large","Large"),
    ("xlarge","Xlarge"),
    ("xxlarge","XXlarge"),
]  
class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()    
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)   
    quantity = models.PositiveIntegerField(default=1) 
    material = models.CharField(null=True, blank=True, max_length=50)
    size = models.CharField(choices=sizes, max_length=15)            
    
    class Meta:
        ordering = ('created_at',)
        
    def __str__(self):
        return self.name 
    
class Query(models.Model):
    name = models.CharField(max_length=255)
    message = models.TextField(blank=False, null=False)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('created_at',)
        
    def __str__(self):
        return self.name 


transaction_status = [
    ("pending","Pending"),
    ("failed","Failed"),
    ("success","Success")
]

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    items = models.ManyToManyField(Item, through='CartItem')
    
    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural = 'Cart'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return self.item.name

# class Transaction(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     items = models.ForeignKey(Item, on_delete=models.CASCADE)
#     razorpay_order_id = models.CharField(max_length=256)
#     user = models.ForeignKey(to=User, on_delete=models.CASCADE)
#     amount = models.FloatField()
#     status = models.CharField(choices=transaction_status, max_length=7)
#     tax = models.FloatField() 
#     created = models.DateTimeField(auto_now_add=True)
