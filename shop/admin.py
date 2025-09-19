from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count, Sum, Q
from django.contrib.admin import SimpleListFilter
from .models import Category, Product, Cart, CartItem, Order, OrderItem

class IsActiveFilter(SimpleListFilter):
    title = 'Status'
    parameter_name = 'is_active'
    
    def lookups(self, request, model_admin):
        return (
            ('active', 'Active'),
            ('inactive', 'Inactive'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'active':
            return queryset.filter(is_active=True)
        elif self.value() == 'inactive':
            return queryset.filter(is_active=False)

class StockFilter(SimpleListFilter):
    title = 'Stock Status'
    parameter_name = 'stock_status'
    
    def lookups(self, request, model_admin):
        return (
            ('in_stock', 'In Stock'),
            ('low_stock', 'Low Stock (< 10)'),
            ('out_of_stock', 'Out of Stock'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'in_stock':
            return queryset.filter(stock__gt=10)
        elif self.value() == 'low_stock':
            return queryset.filter(stock__lte=10, stock__gt=0)
        elif self.value() == 'out_of_stock':
            return queryset.filter(stock=0)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'product_count', 'is_active', 'created_at']
    list_filter = [IsActiveFilter, 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Settings', {
            'fields': ('is_active', 'created_at')
        }),
    )
    
    def product_count(self, obj):
        count = obj.products.count()
        if count > 0:
            url = reverse('admin:shop_product_changelist') + f'?category__id__exact={obj.id}'
            return format_html('<a href="{}">{} products</a>', url, count)
        return '0 products'
    product_count.short_description = 'Products'

class ProductAdmin(admin.ModelAdmin):
    list_display = ['image_thumbnail', 'name', 'category', 'price', 'stock', 'stock_status', 'is_featured', 'is_active', 'edit_links', 'created_at']
    list_filter = [IsActiveFilter, StockFilter, 'is_featured', 'category', 'created_at']
    search_fields = ['name', 'description', 'short_description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'stock', 'is_featured', 'is_active']
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    list_per_page = 25
    actions = ['make_featured', 'make_unfeatured', 'activate_products', 'deactivate_products']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'description', 'short_description')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'stock', 'is_featured', 'is_active')
        }),
        ('Media', {
            'fields': ('image', 'image_preview')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 5px; object-fit: cover;" />',
                obj.image.url
            )
        return format_html('<div style="width: 50px; height: 50px; background: #f8f9fa; border-radius: 5px; display: flex; align-items: center; justify-content: center;"><i class="fas fa-image text-muted"></i></div>')
    image_thumbnail.short_description = 'Image'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; border-radius: 8px;" />',
                obj.image.url
            )
        return 'No image uploaded'
    image_preview.short_description = 'Image Preview'
    
    def stock_status(self, obj):
        if obj.stock == 0:
            return format_html('<span class="badge bg-danger">Out of Stock</span>')
        elif obj.stock <= 10:
            return format_html('<span class="badge bg-warning">Low Stock ({})</span>', obj.stock)
        else:
            return format_html('<span class="badge bg-success">In Stock ({})</span>', obj.stock)
    stock_status.short_description = 'Stock Status'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')
    
    def edit_links(self, obj):
        if obj.pk:
            edit_url = reverse('admin:shop_product_change', args=[obj.pk])
            view_url = reverse('admin:shop_product_change', args=[obj.pk])
            return format_html(
                '<a href="{}" class="btn btn-sm btn-primary me-1" title="Edit Product">'
                '<i class="fas fa-edit"></i> Edit</a>'
                '<a href="{}" class="btn btn-sm btn-info" title="View Product">'
                '<i class="fas fa-eye"></i> View</a>',
                edit_url, view_url
            )
        return '-'
    edit_links.short_description = 'Actions'
    edit_links.allow_tags = True
    
    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} products were marked as featured.')
    make_featured.short_description = "Mark selected products as featured"
    
    def make_unfeatured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} products were unmarked as featured.')
    make_unfeatured.short_description = "Mark selected products as not featured"
    
    def activate_products(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} products were activated.')
    activate_products.short_description = "Activate selected products"
    
    def deactivate_products(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} products were deactivated.')
    deactivate_products.short_description = "Deactivate selected products"
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:  # New product
            self.message_user(request, f'Product "{obj.name}" was created successfully.')
        else:  # Updated product
            self.message_user(request, f'Product "{obj.name}" was updated successfully.')

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'total_price']
    fields = ['product', 'quantity', 'total_price']
    
    def total_price(self, obj):
        if obj.pk:
            return f"${obj.total_price}"
        return "-"
    total_price.short_description = 'Total'

class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_or_session', 'total_items', 'total_price', 'created_at']
    list_filter = ['created_at']
    inlines = [CartItemInline]
    readonly_fields = ['created_at', 'updated_at']
    
    def user_or_session(self, obj):
        if obj.user:
            return format_html('<i class="fas fa-user me-1"></i>{}', obj.user.username)
        else:
            return format_html('<i class="fas fa-key me-1"></i>{}', obj.session_key or 'Anonymous')
    user_or_session.short_description = 'User/Session'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'price', 'quantity', 'get_cost']
    fields = ['product', 'price', 'quantity', 'get_cost']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'email', 'status', 'total_cost', 'item_count', 'created_at', 'order_actions']
    list_filter = ['status', 'created_at', 'city']
    search_fields = ['first_name', 'last_name', 'email', 'id']
    inlines = [OrderItemInline]
    readonly_fields = ['created_at', 'updated_at', 'total_cost', 'item_count']
    list_editable = ['status']
    list_per_page = 25
    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_delivered', 'mark_as_cancelled']
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('user', 'first_name', 'last_name', 'email')
        }),
        ('Shipping Address', {
            'fields': ('address', 'postal_code', 'city')
        }),
        ('Order Details', {
            'fields': ('status', 'total_cost', 'created_at', 'updated_at')
        }),
    )
    
    def customer_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    customer_name.short_description = 'Customer'
    
    def status_badge(self, obj):
        status_colors = {
            'pending': 'warning',
            'processing': 'info',
            'shipped': 'primary',
            'delivered': 'success',
            'cancelled': 'danger'
        }
        color = status_colors.get(obj.status, 'secondary')
        return format_html('<span class="badge bg-{}">{}</span>', color, obj.get_status_display())
    status_badge.short_description = 'Status'
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'
    
    def order_actions(self, obj):
        if obj.pk:
            view_url = reverse('admin:shop_order_change', args=[obj.pk])
            return format_html(
                '<a href="{}" class="btn btn-sm btn-primary" title="View Order">'
                '<i class="fas fa-eye"></i> View</a>',
                view_url
            )
        return '-'
    order_actions.short_description = 'Actions'
    order_actions.allow_tags = True
    
    def mark_as_processing(self, request, queryset):
        updated = queryset.update(status='processing')
        self.message_user(request, f'{updated} orders were marked as processing.')
    mark_as_processing.short_description = "Mark selected orders as processing"
    
    def mark_as_shipped(self, request, queryset):
        updated = queryset.update(status='shipped')
        self.message_user(request, f'{updated} orders were marked as shipped.')
    mark_as_shipped.short_description = "Mark selected orders as shipped"
    
    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f'{updated} orders were marked as delivered.')
    mark_as_delivered.short_description = "Mark selected orders as delivered"
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} orders were marked as cancelled.')
    mark_as_cancelled.short_description = "Mark selected orders as cancelled"

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'price', 'quantity', 'get_cost']
    list_filter = ['order__status', 'order__created_at']
    search_fields = ['product__name', 'order__first_name', 'order__last_name']
    readonly_fields = ['get_cost']

# Customize admin site
admin.site.site_header = "Ipswich Retail Administration"
admin.site.site_title = "Ipswich Retail Admin"
admin.site.index_title = "Welcome to Ipswich Retail Administration"

# Add custom admin views for dashboard
from django.contrib.admin import AdminSite
from django.shortcuts import render
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create a custom admin site with enhanced dashboard
from django.contrib.admin import AdminSite
from django.shortcuts import render
from django.contrib.admin.views.main import ChangeList

class CustomAdminSite(AdminSite):
    def index(self, request, extra_context=None):
        # Get statistics for dashboard
        total_products = Product.objects.count()
        total_categories = Category.objects.count()
        total_orders = Order.objects.count()
        
        # Calculate total revenue by summing all order items
        total_revenue = 0
        for order in Order.objects.all():
            total_revenue += order.total_cost
        
        # Recent products
        recent_products = Product.objects.order_by('-created_at')[:5]
        
        # Low stock products
        low_stock_products = Product.objects.filter(stock__lte=10, stock__gt=0).order_by('stock')[:5]
        
        # Product status counts
        active_products = Product.objects.filter(is_active=True).count()
        inactive_products = Product.objects.filter(is_active=False).count()
        out_of_stock_products = Product.objects.filter(stock=0).count()
        
        extra_context = extra_context or {}
        extra_context.update({
            'total_products': total_products,
            'total_categories': total_categories,
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'recent_products': recent_products,
            'low_stock_products': low_stock_products,
            'active_products': active_products,
            'inactive_products': inactive_products,
            'out_of_stock_products': out_of_stock_products,
        })
        
        return super().index(request, extra_context)
    
    def login(self, request, extra_context=None):
        """
        Display the login form for the given HttpRequest.
        """
        if request.method == 'GET' and self.has_permission(request):
            # Already logged-in, redirect to admin index
            index_path = reverse('admin:index', current_app=self.name)
            return HttpResponseRedirect(index_path)
        
        from django.contrib.auth.views import LoginView
        from django.contrib.auth.forms import AuthenticationForm
        
        context = {
            'title': _('Log in'),
            'app_path': request.get_full_path(),
            'username': request.user.get_username(),
        }
        
        if extra_context is not None:
            context.update(extra_context)
        
        defaults = {
            'extra_context': context,
            'authentication_form': AuthenticationForm,
            'template_name': self.login_template,
        }
        
        return LoginView.as_view(**defaults)(request)

# Create custom admin site instance
custom_admin_site = CustomAdminSite(name='custom_admin')
custom_admin_site.site_header = "Ipswich Retail Administration"
custom_admin_site.site_title = "Ipswich Retail Admin"
custom_admin_site.index_title = "Welcome to Ipswich Retail Administration"

# Configure custom admin site to use our templates
custom_admin_site.login_template = 'admin/login.html'
custom_admin_site.index_template = 'admin/index.html'
custom_admin_site.app_index_template = 'admin/index.html'

# Register models with custom admin site
custom_admin_site.register(Category, CategoryAdmin)
custom_admin_site.register(Product, ProductAdmin)
custom_admin_site.register(Cart, CartAdmin)
custom_admin_site.register(Order, OrderAdmin)
custom_admin_site.register(OrderItem, OrderItemAdmin)