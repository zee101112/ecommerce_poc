// Main JavaScript for Ipswich Retail Shop

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add to cart functionality
    const addToCartForms = document.querySelectorAll('.add-to-cart-form');
    console.log('Found add to cart forms:', addToCartForms.length);
    addToCartForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('Add to cart form submitted');
            const button = this.querySelector('.add-to-cart-btn');
            const originalText = button.innerHTML;
            
            // Show loading state
            button.innerHTML = '<span class="loading"></span> Adding...';
            button.disabled = true;
            
            // Get form data
            const formData = new FormData(this);
            const productId = formData.get('product_id');
            const quantity = formData.get('quantity') || 1;
            
            // Get CSRF token
            const csrfToken = getCookie('csrftoken') || document.querySelector('[name=csrfmiddlewaretoken]').value;
            console.log('CSRF Token:', csrfToken);
            
            // Send AJAX request
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => {
                console.log('Response status:', response.status);
                return response.json();
            })
            .then(data => {
                console.log('Response data:', data);
                if (data.success) {
                    // Show success message
                    showAlert('Product added to cart!', 'success');
                    
                    // Update cart count
                    updateCartCount(data.cart_items_count);
                    
                    // Reset button
                    button.innerHTML = originalText;
                    button.disabled = false;
                } else {
                    // Show error message
                    showAlert(data.message || 'Error adding product to cart', 'danger');
                    
                    // Reset button
                    button.innerHTML = originalText;
                    button.disabled = false;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('Error adding product to cart', 'danger');
                
                // Reset button
                button.innerHTML = originalText;
                button.disabled = false;
            });
        });
    });

    // Cart quantity update
    const quantityInputs = document.querySelectorAll('.quantity-input');
    quantityInputs.forEach(input => {
        // Store previous value for error handling
        input.addEventListener('focus', function() {
            this.dataset.previousValue = this.value;
        });
        
        // Real-time calculation as user types
        input.addEventListener('input', function() {
            const cartItemId = this.dataset.cartItemId;
            const quantity = parseInt(this.value) || 0;
            
            if (quantity < 0) {
                this.value = 0;
                return;
            }
            
            // Get the cart item container
            const cartItem = document.querySelector(`[data-cart-item-id="${cartItemId}"]`).closest('.cart-item');
            
            // Get the price per item from the DOM
            const priceElement = cartItem.querySelector('.col-md-2 .fw-bold.text-success');
            const pricePerItem = parseFloat(priceElement.textContent.replace('$', ''));
            
            // Calculate item total immediately for better UX
            const itemTotal = quantity * pricePerItem;
            
            // Update individual item total immediately
            const totalElement = cartItem.querySelector('.col-md-2 .fw-bold:not(.text-success)');
            if (totalElement) {
                totalElement.textContent = `$${itemTotal.toFixed(2)}`;
                // Add visual feedback
                totalElement.style.transition = 'all 0.3s ease';
                totalElement.style.color = '#28a745';
                setTimeout(() => {
                    totalElement.style.color = '';
                }, 300);
            }
            
            // Recalculate overall cart total immediately
            updateCartTotalFromDOM();
        });
        
        // Handle final change and server update
        input.addEventListener('change', function() {
            const cartItemId = this.dataset.cartItemId;
            const quantity = parseInt(this.value);
            
            // Validate quantity
            if (quantity < 1) {
                this.value = 1;
                updateCartTotalFromDOM();
                return;
            }
            
            // Check stock limit if available
            const maxStock = parseInt(this.getAttribute('max'));
            if (maxStock && quantity > maxStock) {
                this.value = maxStock;
                showAlert(`Maximum stock available: ${maxStock}`, 'warning');
                updateCartTotalFromDOM();
                return;
            }
            
            // Get the cart item container
            const cartItem = document.querySelector(`[data-cart-item-id="${cartItemId}"]`).closest('.cart-item');
            
            // Get the price per item from the DOM
            const priceElement = cartItem.querySelector('.col-md-2 .fw-bold.text-success');
            const pricePerItem = parseFloat(priceElement.textContent.replace('$', ''));
            
            // Calculate item total immediately for better UX
            const itemTotal = quantity * pricePerItem;
            
            // Update individual item total immediately
            const totalElement = cartItem.querySelector('.col-md-2 .fw-bold:not(.text-success)');
            if (totalElement) {
                totalElement.textContent = `$${itemTotal.toFixed(2)}`;
                // Add visual feedback
                totalElement.style.transition = 'all 0.3s ease';
                totalElement.style.color = '#28a745';
                setTimeout(() => {
                    totalElement.style.color = '';
                }, 300);
            }
            
            // Recalculate overall cart total immediately
            updateCartTotalFromDOM();
            
            // Send AJAX request to update quantity on server
            fetch(`/cart/update/${cartItemId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    quantity: quantity
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update with server response for accuracy
                    if (data.item_total !== undefined) {
                        const serverItemTotal = parseFloat(data.item_total);
                        if (totalElement) {
                            totalElement.textContent = `$${serverItemTotal.toFixed(2)}`;
                        }
                    }
                    
                    // Update overall cart total with server data
                    updateCartTotals(data.cart_total);
                    showAlert('Cart updated!', 'success');
                } else {
                    // Revert to previous state on error
                    this.value = this.dataset.previousValue || 1;
                    updateCartTotalFromDOM();
                    showAlert('Error updating cart', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Revert to previous state on error
                this.value = this.dataset.previousValue || 1;
                updateCartTotalFromDOM();
                showAlert('Error updating cart', 'danger');
            });
        });
    });

    // Remove from cart
    const removeButtons = document.querySelectorAll('.remove-from-cart');
    removeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const cartItemId = this.dataset.cartItemId;
            
            if (confirm('Are you sure you want to remove this item from your cart?')) {
                fetch(`/shop/cart/remove/${cartItemId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Remove item from DOM
                        this.closest('.cart-item').remove();
                        
                        // Update cart count
                        updateCartCount(data.cart_items_count);
                        
                        // Update total price
                        updateCartTotals(data.cart_total);
                        
                        showAlert('Item removed from cart', 'success');
                    } else {
                        showAlert('Error removing item from cart', 'danger');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showAlert('Error removing item from cart', 'danger');
                });
            }
        });
    });

    // Search functionality
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const searchInput = this.querySelector('input[name="q"]');
            if (searchInput.value.trim() === '') {
                e.preventDefault();
                showAlert('Please enter a search term', 'warning');
            }
        });
    }

    // Product image zoom (for product detail page)
    const productImages = document.querySelectorAll('.product-image');
    productImages.forEach(img => {
        img.addEventListener('click', function() {
            // Create modal for image zoom
            const modal = document.createElement('div');
            modal.className = 'modal fade';
            modal.innerHTML = `
                <div class="modal-dialog modal-lg modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">${this.alt}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body text-center">
                            <img src="${this.src}" class="img-fluid" alt="${this.alt}">
                        </div>
                    </div>
                </div>
            `;
            
            document.body.appendChild(modal);
            const bsModal = new bootstrap.Modal(modal);
            bsModal.show();
            
            // Remove modal from DOM when hidden
            modal.addEventListener('hidden.bs.modal', function() {
                document.body.removeChild(modal);
            });
        });
    });
});

// Checkout functions
function proceedToCheckout() {
    window.location.href = '/checkout/';
}

function saveForLater() {
    showAlert('Cart saved for later!', 'info');
}

// Utility functions
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showAlert(message, type) {
    const alertContainer = document.querySelector('.alert-container') || createAlertContainer();
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.appendChild(alert);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

function createAlertContainer() {
    const container = document.createElement('div');
    container.className = 'alert-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

function updateCartCount(count) {
    const cartBadge = document.querySelector('.badge');
    if (cartBadge) {
        cartBadge.textContent = count;
    }
}

function updateCartTotals(total) {
    const totalElements = document.querySelectorAll('.cart-total-price');
    const totalValue = parseFloat(total);
    totalElements.forEach(element => {
        element.textContent = `$${totalValue.toFixed(2)}`;
    });
}

function updateCartTotalFromDOM() {
    // Calculate total from all cart items in the DOM
    const cartItems = document.querySelectorAll('.cart-item');
    let total = 0;
    
    cartItems.forEach(item => {
        const quantityInput = item.querySelector('.quantity-input');
        const priceElement = item.querySelector('.col-md-2 .fw-bold.text-success');
        
        if (quantityInput && priceElement) {
            const quantity = parseInt(quantityInput.value) || 0;
            const pricePerItem = parseFloat(priceElement.textContent.replace('$', '')) || 0;
            const itemTotal = quantity * pricePerItem;
            total += itemTotal;
            
            // Update individual item total
            const totalElement = item.querySelector('.col-md-2 .fw-bold:not(.text-success)');
            if (totalElement) {
                totalElement.textContent = `$${itemTotal.toFixed(2)}`;
            }
        }
    });
    
    // Update all cart total elements
    const totalElements = document.querySelectorAll('.cart-total-price');
    totalElements.forEach(element => {
        element.textContent = `$${total.toFixed(2)}`;
    });
    
    return total;
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Lazy loading for images
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

}); // End of DOMContentLoaded
