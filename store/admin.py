from django.contrib import admin
from django.utils.html import format_html, mark_safe
from django.urls import reverse
from .models import Product, Order, OrderItem, UserAddress, Wishlist, WishlistItem, ProductImage

# --- ProductImage Inline Admin with Better UI ---
class ProductImageInline(admin.StackedInline):
    """Professional image management interface"""
    model = ProductImage
    extra = 1
    fields = ('image_url', 'image_preview', 'is_primary', 'display_order', 'help_text')
    readonly_fields = ('image_preview', 'help_text')
    ordering = ('display_order',)
    
    def image_preview(self, obj):
        """Display a preview of the image"""
        if obj.image_url:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; border-radius: 8px; border: 2px solid #ddd; padding: 5px;" />',
                obj.image_url
            )
        return mark_safe('<p style="color: #999;">No image URL provided</p>')
    image_preview.short_description = 'Image Preview'
    
    def help_text(self, obj):
        """Display helpful information"""
        primary_text = '<span style="color: #27ae60; font-weight: bold;">✓ Primary Image</span>' if obj.is_primary else '<span style="color: #999;">This will be displayed in product list</span>'
        return format_html(
            '<div style="padding: 10px; background: #f9f9f9; border-radius: 6px;">'
            '<p><strong>Image Order:</strong> {} (Lower numbers appear first in description)</p>'
            '<p><strong>Status:</strong> {}</p>'
            '</div>',
            obj.display_order,
            primary_text
        )
    help_text.short_description = 'Image Information'

# --- Product Admin with Enhanced UI ---
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock', 'status_badge', 'image_count', 'primary_image_preview')
    search_fields = ('name', 'description')
    list_filter = ('price', 'stock')
    inlines = [ProductImageInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'price', 'stock'),
            'description': 'Enter product details and pricing information'
        }),
        ('Main Image (Legacy)', {
            'fields': ('image_url',),
            'description': '⚠️ This field is deprecated. Use the Images section below to add and manage product images.',
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        """Display stock status with color"""
        if obj.stock > 10:
            color = '#27ae60'
            status = 'In Stock'
        elif obj.stock > 0:
            color = '#f39c12'
            status = 'Low Stock'
        else:
            color = '#e74c3c'
            status = 'Out of Stock'
        
        return format_html(
            '<span style="color: white; background-color: {}; padding: 5px 12px; border-radius: 20px; font-weight: bold;">{}</span>',
            color, status
        )
    status_badge.short_description = 'Stock Status'
    
    def image_count(self, obj):
        """Display number of images"""
        count = obj.images.count()
        primary = obj.images.filter(is_primary=True).exists()
        icon = '✓' if primary else '✗'
        return format_html(
            '<strong>{}</strong> image{} {} Primary',
            count,
            's' if count != 1 else '',
            icon
        )
    image_count.short_description = 'Images (Primary)'
    
    def primary_image_preview(self, obj):
        """Display thumbnail of primary image"""
        primary = obj.images.filter(is_primary=True).first()
        if primary and primary.image_url:
            return format_html(
                '<img src="{}" style="max-width: 50px; max-height: 50px; border-radius: 4px; border: 1px solid #ddd;" />',
                primary.image_url
            )
        return mark_safe('<span style="color: #999;">No primary image</span>')
    primary_image_preview.short_description = 'Preview'

# --- OrderItem Inline Admin ---
class OrderItemInline(admin.StackedInline):
    """Professional order item display"""
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'price', 'quantity', 'item_subtotal')
    fields = ('product', 'price', 'quantity', 'item_subtotal')
    can_delete = False
    
    def item_subtotal(self, obj):
        """Display calculated subtotal"""
        return format_html(
            '<strong style="color: #27ae60; font-size: 1.1em;">₹{}</strong>',
            obj.subtotal()
        )
    item_subtotal.short_description = 'Subtotal'

# --- Order Admin with Enhanced UI ---
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'total_with_currency', 'status_badge', 'order_date', 'action_buttons')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email', 'id')
    readonly_fields = ('user', 'total_price', 'created_at', 'order_summary')
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Order Summary', {
            'fields': ('order_summary',),
            'classes': ('wide',)
        }),
        ('Customer Information', {
            'fields': ('user', 'created_at'),
        }),
        ('Order Total', {
            'fields': ('total_price',),
        }),
        ('Delivery Status', {
            'fields': ('status',),
            'description': '📦 Update the delivery status to notify the customer'
        }),
    )
    
    def order_number(self, obj):
        """Display formatted order number"""
        return format_html(
            '<strong style="font-size: 1.1em;">#{}</strong>',
            obj.id
        )
    order_number.short_description = 'Order #'
    
    def customer_name(self, obj):
        """Display customer name"""
        return obj.user.get_full_name() or obj.user.username
    customer_name.short_description = 'Customer'
    
    def total_with_currency(self, obj):
        """Display total with currency formatting"""
        return format_html(
            '<strong style="color: #27ae60; font-size: 1.1em;">₹{}</strong>',
            obj.total_price
        )
    total_with_currency.short_description = 'Total'
    
    def order_date(self, obj):
        """Display order date in readable format"""
        return obj.created_at.strftime('%d %b %Y, %I:%M %p')
    order_date.short_description = 'Order Date'
    
    def status_badge(self, obj):
        """Display status with professional styling"""
        colors = {
            'Pending': '#FFA500',      # Orange
            'Processing': '#3498DB',   # Blue
            'Shipped': '#9B59B6',      # Purple
            'Delivered': '#27AE60',    # Green
            'Cancelled': '#E74C3C',    # Red
        }
        icons = {
            'Pending': '⏳',
            'Processing': '⚙️',
            'Shipped': '📦',
            'Delivered': '✓',
            'Cancelled': '✗',
        }
        color = colors.get(obj.status, '#95A5A6')
        icon = icons.get(obj.status, '•')
        
        return format_html(
            '<span style="color: white; background-color: {}; padding: 8px 16px; border-radius: 20px; font-weight: bold; display: inline-block;">{} {}</span>',
            color, icon, obj.status
        )
    status_badge.short_description = 'Status'
    
    def action_buttons(self, obj):
        """Display quick action links"""
        details_url = reverse('admin:store_order_change', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="background-color: #3498db; margin-right: 5px;">View Details</a>',
            details_url,
        )
    action_buttons.short_description = 'Actions'
    
    def order_summary(self, obj):
        """Display complete order summary"""
        items_html = '<div style="margin-top: 10px;">'
        for item in obj.orderitem_set.all():
            items_html += format_html(
                '<div style="padding: 8px; background: #f9f9f9; margin: 5px 0; border-radius: 4px;">'
                '<strong>{}</strong> × {} = <span style="color: #27ae60; font-weight: bold;">₹{}</span>'
                '</div>',
                item.product.name, item.quantity, item.subtotal()
            )
        items_html += '</div>'
        
        return format_html(
            '<div style="background: #f0f7ff; padding: 15px; border-radius: 8px; border: 2px solid #3498db;">'
            '<strong style="font-size: 1.2em;">Order Items:</strong>{}'
            '<div style="border-top: 2px solid #ddd; margin-top: 15px; padding-top: 10px;">'
            '<strong>Total: </strong><span style="color: #27ae60; font-weight: bold; font-size: 1.2em;">₹{}</span>'
            '</div>'
            '</div>',
            items_html, obj.total_price
        )
    order_summary.short_description = 'Order Details'

# --- OrderItem Admin (for standalone viewing) ---
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_link', 'product_name', 'price_display', 'quantity', 'subtotal_display')
    list_filter = ('order__created_at',)
    search_fields = ('order__id', 'product__name')
    readonly_fields = ('order', 'product', 'price', 'quantity', 'subtotal_display')
    
    def order_link(self, obj):
        """Display order number as link"""
        return format_html(
            '<strong>Order #{}</strong>',
            obj.order.id
        )
    order_link.short_description = 'Order'
    
    def product_name(self, obj):
        """Display product name"""
        return obj.product.name
    product_name.short_description = 'Product'
    
    def price_display(self, obj):
        """Display price with currency"""
        return format_html(
            '₹<strong>{}</strong>',
            obj.price
        )
    price_display.short_description = 'Price'
    
    def subtotal_display(self, obj):
        """Display subtotal with currency"""
        return format_html(
            '<span style="color: #27ae60; font-weight: bold;">₹{}</span>',
            obj.subtotal()
        )
    subtotal_display.short_description = 'Subtotal'

# --- UserAddress Admin ---
@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('full_name_link', 'phone', 'city_state', 'pin_code', 'status_badge')
    search_fields = ('user__username', 'full_name', 'phone', 'city', 'pin_code')
    list_filter = ('state', 'country', 'created_at')
    readonly_fields = ('created_at', 'updated_at', 'user_display')
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('user_display', 'full_name', 'phone'),
            'description': 'User and contact information'
        }),
        ('Address Details', {
            'fields': ('street_address', 'landmark', 'city', 'state', 'pin_code', 'country'),
            'description': 'Complete address information'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_display(self, obj):
        """Display user information"""
        return format_html(
            '<strong>{}</strong> ({})',
            obj.user.get_full_name() or obj.user.username,
            obj.user.email
        )
    user_display.short_description = 'User'
    
    def full_name_link(self, obj):
        """Display full name"""
        return format_html(
            '<strong>{}</strong>',
            obj.full_name
        )
    full_name_link.short_description = 'Name'
    
    def city_state(self, obj):
        """Display city and state together"""
        return f"{obj.city}, {obj.state}"
    city_state.short_description = 'City, State'
    
    def status_badge(self, obj):
        """Display status badge"""
        return format_html(
            '<span style="color: white; background-color: #27ae60; padding: 5px 10px; border-radius: 15px; font-weight: bold;">✓ Active</span>'
        )
    status_badge.short_description = 'Status'
    
    def has_add_permission(self, request):
        # Users add address from profile, not admin
        return False

# --- Wishlist Item Inline ---
class WishlistItemInline(admin.StackedInline):
    """Display wishlist items in a clean format"""
    model = WishlistItem
    extra = 0
    readonly_fields = ('product_display', 'added_date')
    fields = ('product_display', 'added_date')
    can_delete = True
    
    def product_display(self, obj):
        """Display product with formatting"""
        return format_html(
            '<strong>{}</strong> - <span style="color: #27ae60;">₹{}</span>',
            obj.product.name, obj.product.price
        )
    product_display.short_description = 'Product'
    
    def added_date(self, obj):
        """Display when item was added"""
        return obj.added_at.strftime('%d %b %Y')
    added_date.short_description = 'Added On'

# --- Wishlist Admin ---
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('username', 'item_count_badge', 'created_at_formatted', 'last_modified')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('user', 'created_at', 'wishlists_summary')
    inlines = [WishlistItemInline]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Wishlist Information', {
            'fields': ('user', 'created_at', 'wishlists_summary'),
            'description': 'User wishlist details'
        }),
    )
    
    def username(self, obj):
        """Display username"""
        return format_html(
            '<strong>{}</strong>',
            obj.user.username
        )
    username.short_description = 'Customer'
    
    def item_count_badge(self, obj):
        """Display item count in badge"""
        count = obj.items.count()
        return format_html(
            '<span style="background-color: #3498db; color: white; padding: 5px 12px; border-radius: 15px; font-weight: bold;">{} item{}</span>',
            count, 's' if count != 1 else ''
        )
    item_count_badge.short_description = 'Items'
    
    def created_at_formatted(self, obj):
        """Display creation date"""
        return obj.created_at.strftime('%d %b %Y')
    created_at_formatted.short_description = 'Created On'
    
    def last_modified(self, obj):
        """Display last item added"""
        last_item = obj.items.last()
        if last_item:
            return last_item.added_at.strftime('%d %b %Y')
        return '-'
    last_modified.short_description = 'Last Modified'
    
    def wishlists_summary(self, obj):
        """Display summary of wishlist contents"""
        items = obj.items.all()
        if not items:
            return '<em style="color: #999;">No items in wishlist</em>'
        
        summary = '<div style="background: #f9f9f9; padding: 15px; border-radius: 8px;">'
        for item in items:
            summary += format_html(
                '<div style="padding: 8px; margin: 5px 0; background: white; border-radius: 4px; border-left: 3px solid #3498db;">'
                '<strong>{}</strong><br/>'
                '<small style="color: #999;">Price: ₹{} | Added: {}</small>'
                '</div>',
                item.product.name,
                item.product.price,
                item.added_at.strftime('%d %b %Y')
            )
        summary += '</div>'
        return format_html(summary)
    wishlists_summary.short_description = 'Wishlist Items'
    
    def has_add_permission(self, request):
        return False

# --- WishlistItem Admin ---
@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'customer_name', 'price_display', 'added_at_formatted')
    list_filter = ('added_at',)
    search_fields = ('wishlist__user__username', 'product__name')
    readonly_fields = ('wishlist', 'product', 'added_at')
    
    def product_name(self, obj):
        """Display product name"""
        return format_html(
            '<strong>{}</strong>',
            obj.product.name
        )
    product_name.short_description = 'Product'
    
    def customer_name(self, obj):
        """Display customer name"""
        return obj.wishlist.user.username
    customer_name.short_description = 'Customer'
    
    def price_display(self, obj):
        """Display product price"""
        return format_html(
            '<span style="color: #27ae60; font-weight: bold;">₹{}</span>',
            obj.product.price
        )
    price_display.short_description = 'Price'
    
    def added_at_formatted(self, obj):
        """Display date added"""
        return obj.added_at.strftime('%d %b %Y, %I:%M %p')
    added_at_formatted.short_description = 'Added On'