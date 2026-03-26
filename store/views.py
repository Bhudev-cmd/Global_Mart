from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.models import User
from .models import Product, Cart, CartItem, Order, OrderItem, UserAddress, Wishlist, WishlistItem

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
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

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

@login_required(login_url='login')
def payment_view(request):
    """Payment view with address validation"""
    # Check if user has address
    try:
        address = request.user.address
    except UserAddress.DoesNotExist:
        # Redirect to add address
        return redirect('add_address')
    
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    if not cart_items.exists():
        return redirect('product_list')
        
    total_price = sum(item.subtotal() for item in cart_items)

    if request.method == 'POST':
        # 1. Create the permanent Order record
        order = Order.objects.create(user=request.user, total_price=total_price)

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
        return redirect('order_success')

    return render(request, 'store/payment.html', {'total_price': total_price})

@login_required(login_url='login')
def order_success(request):
    return render(request, 'order_success.html')

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