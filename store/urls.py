from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('signup/', views.signup, name='signup'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase-qty/<int:item_id>/', views.increase_qty, name='increase_qty'),
    path('decrease-qty/<int:item_id>/', views.decrease_qty, name='decrease_qty'),
    path('order-success/', views.order_success, name='order_success'),
    
    # Profile and Address Management
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/add-address/', views.add_address, name='add_address'),
    path('profile/update-address/', views.update_address, name='update_address'),
    
    # Wishlist
    path('wishlist/', views.view_wishlist, name='view_wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    
    # Payment
    path('payment/', views.payment_view, name='payment'),
]