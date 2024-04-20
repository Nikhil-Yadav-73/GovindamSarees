from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
import razorpay
from .models import Item, Category, Query, Cart, CartItem, User, Post, UserProfile
from django.contrib import messages
from govsar.settings import BASE_DIR, coupons
from twilio.rest import Client
from django.conf import settings


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@login_required
def search(request):
    items = Item.objects.all()
    query = request.GET.get('query', '')
    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'search.html', {
        'items': items,
        'query': query,
    })

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    elif request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            pswd = request.POST.get('password')
            user = authenticate(request, username=username, email=email, password=pswd)
            
            if user is not None:
                login(request, user)
                messages.success(request, "You have been logged in successfully")
                return redirect('website:home')
            
            else:
                messages.success(request, "There was an error logging in, please try again")
                return redirect('website:home')
    else : return render(request, 'home.html')

@login_required
def edit_profile(request):
    user = request.user
    userprofile = UserProfile.objects.get(user=user)
    username = request.POST.get('username')
    name = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    if username:
        user.username = username
    if email:
        user.email = email
    if name:
        user.first_name = name
    if phone:
        userprofile.phone = phone
    user.save()
    userprofile.save()
    return render(request, 'user_profile.html', {'userprofile':userprofile})

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pswd = request.POST.get('password')
        p2 = request.POST.get('p2')
        username = request.POST.get('username')
        
        if pswd != p2:
            messages.error(request, "Your passwords don't match!")
            return redirect('website:register')

        try:
            user = User.objects.create_user(email=email, password=pswd, username=username)
            user.save()
            messages.success(request, "You have been registered successfully!")
        except Exception as e:
            messages.error(request, f"There was a problem registering your account: {str(e)}")
            return redirect('website:register')

        # Attempt to authenticate the user
        user = authenticate(request, username=email, password=pswd)
        
        if user is not None:
            login(request, user)
            userprofile = UserProfile.objects.create(user=user) 
            userprofile.save()
            messages.success(request, "You have been logged in successfully!")
            return redirect('website:home.html')
        else:
            messages.error(request, "There was a problem logging you in after registration.")
            return redirect('website:home')  # Or wherever you want to redirect in case of registration failure
        # userprofile = UserProfile.objects.get(user = user)
        # userprofile.save()
    return render(request, 'register.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('website:home')

@login_required
def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'feed.html', {'posts':posts})

@require_POST
def like_post(request):
    if request.method == 'POST' and is_ajax(request=request):
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        users = post.liked_by.all()
        if post.liked_by.filter(id=request.user.id).exists():
            # message bhi daal sakte ho
            return JsonResponse({'error': 'You have already liked this post.'}, status=400)
        post.liked_by.add(request.user)
        post.likes += 1
        post.save()
        return JsonResponse({'likes': post.likes})
    return render(request, 'feed.html')

@require_POST
def like_list(request):
    if request.method == 'POST' and is_ajax(request=request):
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        users =  post.liked_by.all()
        return JsonResponse({'users': users})
    return render(request, 'feed.html')

def comments(request):
    return render(request, 'feed.html')

def guide(request):
    return render(request, 'nav.html')

def test(request):
    return render(request, 'test.html')

def category(request, category):
    cat = Category.objects.filter(name=category).first()
    items = Item.objects.filter(category=cat)
    return render(request, 'category.html', {'category':category, 'items':items})

def query(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        user_query = Query.objects.create(name=name, email=email, phone=phone, message=message)
        user_query.save()
        return redirect('website:home')
    return render(request, 'home.html')

def payment(request):
    if request.method == 'POST':
        client = razorpay.Client(auth=("rzp_test_EKzLoiTs6QfPnv", "Su5hpa3bCyiCgY9xEp6x3JnA"))
        payment = client.order.create({
        'amount': 50000,
        'currency': 'INR',
        'payment_capture': '1'
        })
        payment.save()
       
    return render(request, 'payment.html')

def cart(request):
    cart, created = Cart.objects.filter(user=request.user)
    return render (request, 'cart.html')


@login_required
def add_to_cart(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    item = get_object_or_404(Item, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return render(request, 'itemdesc.html', {'product':item})

def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('website:view_cart')

sizes = [
    ("Small"),
    ("Medium"),
    ("Large"),
    ("Xlarge"),
    ("XXlarge"),
]  

@login_required
def item_desc(request, pk):
    product = Item.objects.get(id = pk)
    similar = Item.objects.filter(Q(category=product.category) & ~Q(id = product.id))
    return render(request, 'itemdesc.html', {'product':product, 'sizes':sizes, 'similar':similar})

def view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return render(request, 'viewcart.html')
    cart_items = cart.cartitem_set.all()
    reco = Item.objects.all()
    totalprice = 0.0
    discount = 0.0
    if request.method == 'POST':
        code = request.POST.get('coupon_code')
        discount += coupons[code]
    tax = 0.0
    final = 0.0
    items = []
    for cart_item in cart_items:
        totalprice += cart_item.item.price * cart_item.quantity
        discount += 20
        items.append(cart_item.item)
    tax = totalprice*(.18)
    final = totalprice + tax - discount
    return render(request, 'viewcart.html', {'items':items, 'reco':reco,
    'totalprice':totalprice, 'discount':discount, 'tax':tax, 'final':final})

def remove_item(request, pk):
    try:
        item = Item.objects.get(id=pk)
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, item=item)
        print(cart_item)
        cart_item.delete()
        cart.save()
    except Exception as e:
        return render(request, 'viewcart.html')
    return redirect('website:view_cart')

def user_profile(request):
    user = User.objects.get(id = request.user.id)
    userprofile = UserProfile.objects.get(user = request.user)
    if request.method == 'POST':
        if request.POST['user_name'] :
            user_name = request.POST.get('user_name')
            user.username = user_name
        if request.POST['fullname'] :
            fullname = request.POST.get('fullname')
            user.first_name = fullname
        if request.POST['email'] :
            email = request.POST.get('email')
            user.email = email
        if request.POST['phone'] :
            phone = request.POST.get('phone')
            userprofile.phone = phone
        user.save()
        userprofile.save()
    user = User.objects.get(id = request.user.id)
    userprofile = UserProfile.objects.get(user = request.user)
    return render(request, 'user_profile.html', {'user':user, 'userprofile':userprofile})

def change_pfp(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        print(image)
        userprofile = get_object_or_404(UserProfile, user=request.user)
        if image:
            userprofile.pfp = image
            userprofile.save()
            print(userprofile.pfp.url)
        return render(request, 'user_profile.html', {'userprofile':userprofile})
        
    return render(request, 'change_pfp.html')

@login_required
def new_post(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        title = request.POST.get('title')
        description = request.POST.get('description')
        post = Post.objects.create(image=image, description=description, title=title)
        post.save()
        posts = Post.objects.all()
        return redirect('website:feed')
    return render(request, 'new_post.html')

def change_qty(request):
    if request.method == 'POST' and is_ajax(request=request):
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        
        item = Item.objects.get(id=item_id)
        cart = Cart.objects.get(user=request.user)
        cart_item = cart.cartitem_set.get(item=item)
        print(cart_item.quantity)

        if action == "increaseBtn":
            if cart_item.quantity < item.quantity:
                cart_item.quantity += 1
            else:
                return JsonResponse({'error': 'You can\'t get more than this quantity of this item.'}, status=400)
        elif action == "decreaseBtn":
            if cart_item.quantity > 0:
                cart_item.quantity -= 1
            else:
                cart_item.delete()
                item.save()
                cart.save()
                return redirect('website:view_cart')
            
        item.save()
        cart_item.save()
        cart.save()
        print(cart_item.quantity)
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
        final = totalprice + tax - discount
        return render(request, 'viewcart.html', {'items':items,
        'totalprice':totalprice, 'discount':discount, 'tax':tax, 'final':final})
    return JsonResponse({'error': 'Invalid request.'})

# Function to send verification code via Twilio
def send_verification_code(phone_number, verification_code):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=f"Your verification code is: {verification_code}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )

    return message.sid


# View to initiate phone number verification
def verify_phone_number(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        verification_code = '69069'  # You can generate a random verification code here
        phone_number = "+91"+phone_number
        print(phone_number)
        # Store verification code somewhere (e.g., in session)
        request.session['verification_code'] = verification_code
        request.session['phone_number'] = phone_number

        send_verification_code(phone_number, verification_code)
        return redirect('website:verify_code')

    return render(request, 'verify_phone_number.html')


# View to verify the verification code
def verify_code(request):
    if request.method == 'POST':
        user_entered_code = request.POST.get('verification_code')
        stored_code = request.session.get('verification_code')
        if user_entered_code == stored_code:
            messages.success(request, "Phone number verified successfully!")
        else:
            messages.error(request, "Verification code is incorrect. Please try again.")

        return redirect('website:verify_phone_number')

    return render(request, 'verify_code.html')