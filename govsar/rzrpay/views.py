from django.shortcuts import render, redirect
import razorpay
from .models import Transaction, User
from website.models import Cart, CartItem, UserProfile
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
RAZORPAY = razorpay.Client(auth=('rzp_test_R5IjeUwu0A2DWh','Q8iXWpbh62utu9pgD9KPa4X3'))

def bill(request, user_id):
    user = User.objects.get(id=user_id)
    user_profile = UserProfile.objects.get(user=request.user)
    cart = Cart.objects.get(user = user)
    cart_items = cart.cartitem_set.all()
    totalprice = 0.0
    discount = 0.0
    tax = 0.0
    final = 0.0
    items = []
    for cart_item in cart_items:
        totalprice += cart_item.item.price * cart_item.quantity
        discount += 20
        items.append(cart_item.item)
    tax = totalprice*(.18)
    final = int(totalprice + tax - discount)
    final_amt = final * 100
    bill = {
        'user_profile':user_profile,
        'user':request.user,
        'tax': tax,
        'final': final,
        'discount': discount,
        'totalprice': totalprice,
        }
    if request.method == 'POST':  
        client = razorpay.Client(auth = ("rzp_test_R5IjeUwu0A2DWh", "Q8iXWpbh62utu9pgD9KPa4X3"))
        payment = client.order.create({'amount':final_amt, 'currency':'INR', 'payment_capture':1})
        transaction = Transaction(amount=final_amt, razorpay_order_id=payment['id'], user=request.user, tax=tax, status='pending')
        transaction.save()
        callback_url = 'http://localhost:8000/pay/payment_success'
        return render(request, 'bill.html', {'bill':bill, 'items':items,'payment':payment, 'transaction':transaction, 'callback_url':callback_url})
    return render(request, 'bill.html', {'bill':bill, 'items':items})


@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        return render(request, 'confirmation.html')