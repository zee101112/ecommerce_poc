from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
import json

from .models import Product, Category, Cart, CartItem, Order, OrderItem
from .forms import AddToCartForm, CheckoutForm


def get_or_create_cart(request):
    """Get or create cart for the current user/session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # Ensure session is initialized
        if not request.session.session_key:
            request.session.create()
        
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
    categories = Category.objects.filter(is_active=True)[:6]
    
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
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('name')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_slug,
        'sort_by': sort_by,
    }
    
    return render(request, 'shop/product_list.html', context)

def product_detail(request, slug):
    """Product detail page"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]
    
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            cart = get_or_create_cart(request)
            quantity = form.cleaned_data['quantity']
            
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            messages.success(request, f'{product.name} added to cart!')
            return redirect('shop:cart')
    else:
        form = AddToCartForm()
    
    context = {
        'product': product,
        'related_products': related_products,
        'form': form,
    }
    
    return render(request, 'shop/product_detail.html', context)

def product_list_by_category(request, slug):
    """Product list filtered by category"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(category=category, is_active=True)
    
    # Search within category
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        'products': products,
        'category': category,
        'search_query': search_query,
    }
    
    return render(request, 'shop/product_list.html', context)

def cart(request):
    """Shopping cart page"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    # Clean up duplicate cart items for the same product
    products_in_cart = {}
    items_to_delete = []
    
    for item in cart_items:
        if item.product.id in products_in_cart:
            # Merge quantities and mark for deletion
            products_in_cart[item.product.id].quantity += item.quantity
            products_in_cart[item.product.id].save()
            items_to_delete.append(item)
        else:
            products_in_cart[item.product.id] = item
    
    # Delete duplicate items
    for item in items_to_delete:
        item.delete()
    
    # Refresh cart items after cleanup
    cart_items = cart.items.all()
    
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        
        try:
            cart_item = cart_items.get(id=item_id)
            if action == 'update':
                quantity = int(request.POST.get('quantity', 1))
                if quantity > 0:
                    cart_item.quantity = quantity
                    cart_item.save()
                else:
                    cart_item.delete()
            elif action == 'remove':
                cart_item.delete()
            
            messages.success(request, 'Cart updated!')
        except CartItem.DoesNotExist:
            messages.error(request, 'Item not found in cart.')
        
        return redirect('shop:cart')
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    
    return render(request, 'shop/cart.html', context)

@csrf_exempt
def update_cart(request):
    """AJAX endpoint to update cart"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            quantity = int(data.get('quantity', 1))
            
            cart = get_or_create_cart(request)
            cart_item = cart.items.get(id=item_id)
            
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete()
            
            return JsonResponse({
                'success': True,
                'cart_total': cart.total_price,
                'cart_items_count': cart.total_items
            })
        except (CartItem.DoesNotExist, ValueError, KeyError):
            return JsonResponse({'success': False, 'error': 'Invalid request'})
    
    return JsonResponse({'success': False, 'error': 'Invalid method'})

def checkout(request):
    """Checkout page"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('shop:cart')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create order from form data
            order = Order.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                postal_code=form.cleaned_data['postal_code'],
                city=form.cleaned_data['city'],
                user=request.user if request.user.is_authenticated else None
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
            cart.items.all().delete()
            if 'cart_id' in request.session:
                del request.session['cart_id']
            
            messages.success(request, f'Order #{order.id} placed successfully!')
            return redirect('shop:order_detail', order_id=order.id)
    else:
        form = CheckoutForm(user=request.user)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'form': form,
    }
    
    return render(request, 'shop/checkout.html', context)

@login_required
def order_history(request):
    """User's order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    
    return render(request, 'shop/order_history.html', context)

def order_detail(request, order_id):
    """Order detail page"""
    order = get_object_or_404(Order, id=order_id)
    
    # Check if user can view this order
    if request.user.is_authenticated and order.user != request.user:
        messages.error(request, 'You do not have permission to view this order.')
        return redirect('shop:order_history')
    
    context = {
        'order': order,
    }
    
    return render(request, 'shop/order_detail.html', context)

def add_to_cart(request):
    """Add item to cart"""
    if request.method == 'POST':
        try:
            # Check if this is an AJAX request
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            
            # Handle both form data and JSON data
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                product_id = data.get('product_id')
                quantity = int(data.get('quantity', 1))
            else:
                # Handle regular form data
                product_id = request.POST.get('product_id')
                quantity = int(request.POST.get('quantity', 1))
            
            if not product_id:
                if is_ajax or request.content_type == 'application/json':
                    return JsonResponse({
                        'success': False,
                        'message': 'Product ID is required.'
                    })
                else:
                    messages.error(request, 'Product ID is required.')
                    return redirect('shop:product_list')
            
            product = get_object_or_404(Product, id=product_id, is_active=True)
            cart = get_or_create_cart(request)
            
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            if is_ajax or request.content_type == 'application/json':
                return JsonResponse({
                    'success': True,
                    'message': f'{product.name} added to cart!',
                    'cart_total': cart.total_price,
                    'cart_items_count': cart.total_items
                })
            else:
                messages.success(request, f'{quantity} x {product.name} added to cart.')
                return redirect('shop:cart')
            
        except (Product.DoesNotExist, ValueError, KeyError):
            if is_ajax or request.content_type == 'application/json':
                return JsonResponse({'success': False, 'error': 'Invalid request'})
            else:
                messages.error(request, 'Error adding item to cart.')
                return redirect('shop:product_list')
    
    # Check if this is an AJAX request for error handling
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax or request.content_type == 'application/json':
        return JsonResponse({'success': False, 'error': 'Invalid method'})
    else:
        return redirect('shop:product_list')

@csrf_exempt
def update_cart_item(request, cart_item_id):
    """Update cart item quantity"""
    if request.method == 'POST':
        try:
            # Check if this is an AJAX request
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            
            cart = get_or_create_cart(request)
            cart_item = cart.items.get(id=cart_item_id)
            
            # Handle both JSON and form data
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                quantity = int(data.get('quantity', 1))
            else:
                quantity = int(request.POST.get('quantity', 1))
            
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
                item_total = cart_item.total_price
            else:
                item_total = 0
                cart_item.delete()
            
            # Refresh cart from database to get updated totals
            cart.refresh_from_db()
            
            if is_ajax or request.content_type == 'application/json':
                return JsonResponse({
                    'success': True,
                    'message': 'Cart updated!',
                    'cart_total': cart.total_price,
                    'cart_items_count': cart.total_items,
                    'item_total': item_total
                })
            else:
                messages.success(request, 'Cart updated!')
                return redirect('shop:cart')
        except CartItem.DoesNotExist:
            if is_ajax or request.content_type == 'application/json':
                return JsonResponse({
                    'success': False,
                    'message': 'Item not found in cart.'
                })
            else:
                messages.error(request, 'Item not found in cart.')
                return redirect('shop:cart')
    
    # Check if this is an AJAX request for error handling
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax or request.content_type == 'application/json':
        return JsonResponse({'success': False, 'message': 'Invalid method'})
    else:
        return redirect('shop:cart')

def remove_from_cart(request, cart_item_id):
    """Remove item from cart"""
    if request.method == 'POST':
        try:
            # Check if this is an AJAX request
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            
            cart = get_or_create_cart(request)
            cart_item = cart.items.get(id=cart_item_id)
            cart_item.delete()
            
            if is_ajax or request.content_type == 'application/json':
                return JsonResponse({
                    'success': True,
                    'message': 'Item removed from cart!',
                    'cart_total': cart.total_price,
                    'cart_items_count': cart.total_items
                })
            else:
                messages.success(request, 'Item removed from cart!')
                return redirect('shop:cart')
        except CartItem.DoesNotExist:
            if is_ajax or request.content_type == 'application/json':
                return JsonResponse({
                    'success': False,
                    'message': 'Item not found in cart.'
                })
            else:
                messages.error(request, 'Item not found in cart.')
                return redirect('shop:cart')
    
    # Check if this is an AJAX request for error handling
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax or request.content_type == 'application/json':
        return JsonResponse({'success': False, 'message': 'Invalid method'})
    else:
        return redirect('shop:cart')