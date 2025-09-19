from .models import Cart

def cart_context(request):
    """Add cart information to all templates"""
    cart_items_count = 0
    categories = []
    
    try:
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
        
        if cart:
            cart_items_count = cart.total_items
    except:
        cart_items_count = 0
    
    # Get active categories for navigation
    from .models import Category
    try:
        categories = Category.objects.filter(is_active=True)[:6]
    except:
        categories = []
    
    return {
        'cart_items_count': cart_items_count,
        'categories': categories,
    }
