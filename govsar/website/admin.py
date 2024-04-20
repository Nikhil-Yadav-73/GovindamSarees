from django.contrib import admin
from .models import Post, Item, Category, Query, Cart, CartItem, UserProfile

admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Query)