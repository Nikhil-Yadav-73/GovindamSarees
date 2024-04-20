from django.urls import path, include
from . import views

app_name='website'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('feed/', views.feed, name='feed'),
    path('', views.home, name = 'home'),
    path('register/', views.register, name='register'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('search/', views.search, name = 'search'),
    path('query/', views.query, name='query'),
    path('test/', views.test, name='test'),
    path('<str:category>', views.category, name='category'),
    path('payment/', views.payment, name='payment'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('item_desc/<int:pk>', views.item_desc, name='item_desc'),
    path('like_post/', views.like_post, name='like_post'),
    path('like_list/', views.like_list, name='like_list'),
    path('comments/', views.comments, name='comments'),
    path('new_post/', views.new_post, name='new_post'),
    path('remove_item/<int:pk>', views.remove_item, name='remove_item'),
    path('change_pfp/', views.change_pfp, name='change_pfp'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_qty/', views.change_qty, name='change_qty'),
    path('verify/', views.verify_phone_number, name='verify_phone_number'),
    path('verify/code/', views.verify_code, name='verify_code'),
]
