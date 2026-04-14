from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.core.paginator import Paginator
from django import forms
from django.contrib.auth.models import User
from decimal import Decimal
import base64
import hashlib
import hmac
import json
import time
import urllib.error
import urllib.request
from .models import Category, Product, Cart, CartItem, Order, OrderItem, UserAddress, Wishlist, WishlistItem

# ==========================================
# FORMS
# ==========================================

class UserAddressForm(forms.ModelForm):
    country = forms.CharField(
        initial='India',
        widget=forms.HiddenInput()
    )
    
    class Meta:
        model = UserAddress
        fields = ['full_name', 'phone', 'street_address', 'landmark', 'city', 'state', 'pin_code', 'country']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Enter your full name', 'maxlength': '100'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter phone number', 'maxlength': '20'}),
            'street_address': forms.Textarea(attrs={'placeholder': 'House No., Building, Apartment, Road Name', 'rows': 3, 'maxlength': '255'}),
            'landmark': forms.TextInput(attrs={'placeholder': 'e.g., Near Central Mall', 'maxlength': '200'}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter city name', 'maxlength': '100'}),
            'state': forms.TextInput(attrs={'placeholder': 'Enter state name', 'maxlength': '100'}),
            'pin_code': forms.TextInput(attrs={'placeholder': 'Enter PIN code', 'maxlength': '6'}),
        }

class UserProfileForm(forms.ModelForm):
    """Form to edit user profile information"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email address'}),
        }

# ==========================================
# VIEWS
# ==========================================

def product_list(request):
    query = request.GET.get('search')
    category_id = request.GET.get('category')
    page_number = request.GET.get('page', 1)
    
    products = Product.objects.all().order_by('id')
    categories = Category.objects.all()
    selected_category = None
    
    # Filter by category if provided
    if category_id:
        selected_category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=selected_category)
    
    # Filter by search query if provided
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()

    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'store/product_list.html', {
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': query
    })

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'store/signup.html', {'form': form})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

# --- Shopping Cart Views ---

@login_required(login_url='login')
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.subtotal() for item in cart_items)
    context = {'cart_items': cart_items, 'total_price': total_price}
    return render(request, 'cart.html', context)

@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')

@login_required(login_url='login')
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart_detail')

@login_required(login_url='login')
def increase_qty(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')

@login_required(login_url='login')
def decrease_qty(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_detail')

# --- Payment and Checkout Views ---

def _current_cart_total(user):
    cart = get_object_or_404(Cart, user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum((item.subtotal() for item in cart_items), Decimal('0.00'))
    return cart, cart_items, total_price


def _create_razorpay_order(amount_paise, receipt):
    payload = json.dumps({
        'amount': amount_paise,
        'currency': 'INR',
        'receipt': receipt,
        'payment_capture': 1,
    }).encode('utf-8')

    auth_pair = f"{settings.RAZORPAY_KEY_ID}:{settings.RAZORPAY_KEY_SECRET}".encode('utf-8')
    auth_header = base64.b64encode(auth_pair).decode('utf-8')

    request = urllib.request.Request(
        'https://api.razorpay.com/v1/orders',
        data=payload,
        method='POST',
        headers={
            'Authorization': f'Basic {auth_header}',
            'Content-Type': 'application/json',
        },
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode('utf-8'))


@login_required(login_url='login')
@require_POST
def create_razorpay_order(request):
    if settings.RAZORPAY_MODE != 'live':
        return JsonResponse({'error': 'Razorpay is in mock mode.'}, status=400)

    if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
        return JsonResponse({'error': 'Razorpay keys are missing in environment.'}, status=500)

    try:
        request.user.address
    except UserAddress.DoesNotExist:
        return JsonResponse({'error': 'Please add your delivery address first.'}, status=400)

    _, cart_items, total_price = _current_cart_total(request.user)
    if not cart_items.exists():
        return JsonResponse({'error': 'Cart is empty.'}, status=400)

    amount_paise = int(total_price * 100)
    receipt = f'gm_{request.user.id}_{int(time.time())}'

    try:
        razorpay_order = _create_razorpay_order(amount_paise, receipt)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode('utf-8', errors='ignore')
        return JsonResponse({'error': body or 'Unable to create Razorpay order.'}, status=502)
    except Exception:
        return JsonResponse({'error': 'Unable to create Razorpay order.'}, status=502)

    request.session['razorpay_order_id'] = razorpay_order.get('id', '')
    request.session['razorpay_amount_paise'] = amount_paise

    return JsonResponse({
        'key': settings.RAZORPAY_KEY_ID,
        'order_id': razorpay_order.get('id'),
        'amount': amount_paise,
        'currency': 'INR',
        'prefill': {
            'name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
            'contact': getattr(getattr(request.user, 'address', None), 'phone', ''),
        },
    })

@login_required(login_url='login')
def payment_view(request):
    """Payment view with address validation"""
    # Check if user has address
    try:
        address = request.user.address
    except UserAddress.DoesNotExist:
        # Redirect to add address
        return redirect('add_address')
    
    cart, cart_items, total_price = _current_cart_total(request.user)
    
    if not cart_items.exists():
        return redirect('product_list')
        
    if request.method == 'POST':
        gateway = request.POST.get('gateway', 'razorpay')
        payment_ref = request.POST.get('payment_ref', '').strip()
        payment_method = 'Razorpay'

        if gateway != 'razorpay':
            return render(request, 'store/payment.html', {
                'total_price': total_price,
                'razorpay_mode': settings.RAZORPAY_MODE,
                'payment_error': 'Only Razorpay is available at checkout.'
            })

        if settings.RAZORPAY_MODE == 'live':
            razorpay_payment_id = request.POST.get('razorpay_payment_id', '').strip()
            razorpay_order_id = request.POST.get('razorpay_order_id', '').strip()
            razorpay_signature = request.POST.get('razorpay_signature', '').strip()

            expected_order_id = request.session.get('razorpay_order_id', '')

            if not (razorpay_payment_id and razorpay_order_id and razorpay_signature):
                return render(request, 'store/payment.html', {
                    'total_price': total_price,
                    'razorpay_mode': settings.RAZORPAY_MODE,
                    'payment_error': 'Razorpay payment response is incomplete. Please try again.'
                })

            if not expected_order_id or razorpay_order_id != expected_order_id:
                return render(request, 'store/payment.html', {
                    'total_price': total_price,
                    'razorpay_mode': settings.RAZORPAY_MODE,
                    'payment_error': 'Payment order mismatch. Please retry payment.'
                })

            data = f'{razorpay_order_id}|{razorpay_payment_id}'.encode('utf-8')
            generated_signature = hmac.new(
                settings.RAZORPAY_KEY_SECRET.encode('utf-8'),
                data,
                hashlib.sha256
            ).hexdigest()

            if not hmac.compare_digest(generated_signature, razorpay_signature):
                return render(request, 'store/payment.html', {
                    'total_price': total_price,
                    'razorpay_mode': settings.RAZORPAY_MODE,
                    'payment_error': 'Razorpay verification failed. Please contact support.'
                })

            payment_ref = razorpay_payment_id
        else:
            if not payment_ref:
                return render(request, 'store/payment.html', {
                    'total_price': total_price,
                    'razorpay_mode': settings.RAZORPAY_MODE,
                    'payment_error': 'Razorpay simulation failed. Please try again.'
                })

        # 1. Create the permanent Order record
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            payment_method=payment_method
        )

        # 2. Move items from Cart to OrderItems
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )

        # 3. Empty the cart
        cart_items.delete()
        request.session.pop('razorpay_order_id', None)
        request.session.pop('razorpay_amount_paise', None)
        request.session['last_payment_method'] = payment_method
        return redirect('order_success')

    return render(request, 'store/payment.html', {
        'total_price': total_price,
        'razorpay_mode': settings.RAZORPAY_MODE,
    })

@login_required(login_url='login')
def order_success(request):
    payment_method = request.session.pop('last_payment_method', None)
    return render(request, 'order_success.html', {'payment_method': payment_method})

# --- Profile and History Views ---

@login_required(login_url='login')
def profile_view(request):
    """Display user profile and order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders,
        'user': request.user,
    }
    return render(request, 'store/profile.html', context)

@login_required(login_url='login')
def order_history(request):
    # This view is for your 'orders.html' page
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders.html', {'orders': orders})

# --- Address Management Views ---

@login_required(login_url='login')
def add_address(request):
    """Add a new delivery address - simplified version"""
    try:
        address = request.user.address
        return redirect('update_address')
    except UserAddress.DoesNotExist:
        if request.method == 'POST':
            # Direct save without Django forms
            UserAddress.objects.create(
                user=request.user,
                full_name=request.POST.get('full_name', '').strip(),
                phone=request.POST.get('phone', '').strip(),
                street_address=request.POST.get('street_address', '').strip(),
                landmark=request.POST.get('landmark', '').strip(),
                city=request.POST.get('city', '').strip(),
                state=request.POST.get('state', '').strip(),
                pin_code=request.POST.get('pin_code', '').strip(),
                country='India'
            )
            return redirect('profile')
        return render(request, 'store/address_new.html', {})

@login_required(login_url='login')
def update_address(request):
    """Update existing delivery address - simplified version"""
    try:
        address = request.user.address
    except UserAddress.DoesNotExist:
        return redirect('add_address')
    
    if request.method == 'POST':
        # Direct update without Django forms
        address.full_name = request.POST.get('full_name', '').strip()
        address.phone = request.POST.get('phone', '').strip()
        address.street_address = request.POST.get('street_address', '').strip()
        address.landmark = request.POST.get('landmark', '').strip()
        address.city = request.POST.get('city', '').strip()
        address.state = request.POST.get('state', '').strip()
        address.pin_code = request.POST.get('pin_code', '').strip()
        address.save()
        return redirect('profile')
    
    context = {
        'address': address
    }
    return render(request, 'store/address_new.html', context)

# --- Edit Profile Info View ---

@login_required(login_url='login')
def edit_profile(request):
    """Edit user profile information"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'store/edit_profile.html', {'form': form})

# --- Wishlist Views ---

@login_required(login_url='login')
def view_wishlist(request):
    """View user's wishlist"""
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist_items = wishlist.items.all()
    return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items})

@login_required(login_url='login')
def add_to_wishlist(request, product_id):
    """Add product to wishlist"""
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    wishlist_item, created = WishlistItem.objects.get_or_create(
        wishlist=wishlist,
        product=product
    )
    
    return redirect('view_wishlist')

@login_required(login_url='login')
def remove_from_wishlist(request, item_id):
    """Remove product from wishlist"""
    wishlist_item = get_object_or_404(WishlistItem, id=item_id, wishlist__user=request.user)
    wishlist_item.delete()
    return redirect('view_wishlist')