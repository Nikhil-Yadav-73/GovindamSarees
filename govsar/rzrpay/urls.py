from django.urls import path
from .views import bill, payment_success

app_name = 'rzrpay'

urlpatterns = [
    # path('pay_with_razorpay/<int:user_id>', pay_with_razorpay, name='pay_with_razorpay'),
    path('bill/<int:user_id>', bill, name='bill'),
    path('payment_success/', payment_success, name='payment_success'),
    path('pat/payment_success/', payment_success, name='payment_success'),
]
