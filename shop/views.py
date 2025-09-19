from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json

from .models import Product, Category, Cart, CartItem, Order, OrderItem
from .forms import AddToCartForm, CheckoutForm

def get_or_create_cart(request):
    """Get or create cart for the current user/session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            try:
                cart = Cart.objects.get(id=cart_id)
            except Cart.DoesNotExist:
                cart = None
        else:
            cart = None
        
        if not cart:
            cart = Cart.objects.create(session_key=request.session.session_key)
            request.session['cart_id'] = cart.id
    
    return cart

def home(request):
    """Home page with featured products"""
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:6]
    categories = Category.objects.filter(is_active=True)[:4]
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'shop/home.html', context)

def product_list(request):
    """Product list page with search and filtering"""
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(short_description__icontains=search_query)
        )
    
    # Category filtering
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # Price filtering
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Sorting
    sort_by = request.GET.get('sort', 'created_at')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_slug,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
    }
    return render(request, 'shop/product_list.html', context)

def product_list_by_category(request, category_slug):
    """Product list filtered by category"""
    category = get_object_or_404(Category, slug=category_slug, is_active=True)
    products = Product.objects.filter(category=category, is_active=True)
    categories = Category.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(short_description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'categories': categories,
        'current_category': category,
        'search_query': search_query,
    }
    return render(request, 'shop/product_list.html', context)

def product_detail(request, slug):
    """Product detail page"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product.id)[:4]
    
    # Add to cart form
    add_to_cart_form = AddToCartForm()
    
    context = {
        'product': product,
        'related_products': related_products,
        'add_to_cart_form': add_to_cart_form,
    }
    return render(request, 'shop/product_detail.html', context)

@require_POST
def add_to_cart(request):
    """Add product to cart via AJAX"""
    try:
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        product = get_object_or_404(Product, id=product_id, is_active=True)
        
        if not product.in_stock:
            return JsonResponse({
                'success': False,
                'message': 'Product is out of stock'
            })
        
        cart = get_or_create_cart(request)
        
        # Check if item already exists in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Product added to cart successfully',
            'cart_items_count': cart.total_items
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error adding product to cart'
        })

def cart(request):
    """Shopping cart page"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'shop/cart.html', context)

@require_POST
def update_cart_item(request, cart_item_id):
    """Update cart item quantity via AJAX"""
    try:
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))
        
        if quantity < 1:
            quantity = 1
        
        cart_item.quantity = quantity
        cart_item.save()
        
        return JsonResponse({
            'success': True,
            'cart_total': float(cart_item.cart.total_price)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error updating cart item'
        })

@require_POST
def remove_from_cart(request, cart_item_id):
    """Remove item from cart via AJAX"""
    try:
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        cart = cart_item.cart
        cart_item.delete()
        
        return JsonResponse({
            'success': True,
            'cart_items_count': cart.total_items,
            'cart_total': float(cart.total_price)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error removing item from cart'
        })

def checkout(request):
    """Checkout page"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    if not cart_items:
        messages.warning(request, 'Your cart is empty.')
        return redirect('shop:cart')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST, user=request.user)
        if form.is_valid():
            # Create order
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                postal_code=form.cleaned_data['postal_code'],
                city=form.cleaned_data['city'],
                status='pending'
            )
            
            # Create order items
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    price=cart_item.product.price,
                    quantity=cart_item.quantity
                )
            
            # Clear cart
            cart_items.delete()
            cart.delete()
            
            messages.success(request, f'Order #{order.id} placed successfully!')
            return redirect('shop:order_detail', order_id=order.id)
    else:
        form = CheckoutForm(user=request.user)
    
    context = {
        'form': form,
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'shop/checkout.html', context)

def order_detail(request, order_id):
    """Order detail page"""
    order = get_object_or_404(Order, id=order_id)
    
    # Check if user can view this order
    if request.user.is_authenticated:
        if order.user != request.user:
            messages.error(request, 'You do not have permission to view this order.')
            return redirect('shop:home')
    else:
        # For anonymous users, we could implement a token-based system
        # For now, we'll allow viewing but this should be secured in production
        pass
    
    context = {
        'order': order,
        'order_items': order.items.all(),
    }
    return render(request, 'shop/order_detail.html', context)

@login_required
def order_history(request):
    """User's order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'shop/order_history.html', context)