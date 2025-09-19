from django import forms
from .models import Product

class AddToCartForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(
        min_value=1,
        max_value=99,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'max': '99',
            'value': '1'
        })
    )

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:
            raise forms.ValidationError('Quantity must be at least 1')
        if quantity > 99:
            raise forms.ValidationError('Quantity cannot exceed 99')
        return quantity

    def clean(self):
        cleaned_data = super().clean()
        product_id = cleaned_data.get('product_id')
        quantity = cleaned_data.get('quantity')
        
        if product_id and quantity:
            try:
                product = Product.objects.get(id=product_id, is_active=True)
                if not product.in_stock:
                    raise forms.ValidationError('This product is currently out of stock')
                if quantity > product.stock:
                    raise forms.ValidationError(f'Only {product.stock} items available in stock')
            except Product.DoesNotExist:
                raise forms.ValidationError('Product not found')
        
        return cleaned_data

class CheckoutForm(forms.Form):
    first_name = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'First Name',
            'required': True
        })
    )
    last_name = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Last Name',
            'required': True
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Email Address',
            'required': True
        })
    )
    address = forms.CharField(
        max_length=250, 
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'placeholder': 'Street Address', 
            'rows': 3,
            'required': True
        })
    )
    postal_code = forms.CharField(
        max_length=20, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Postal Code',
            'required': True
        })
    )
    city = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'City',
            'required': True
        })
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Pre-fill form with user data if available
        if user and user.is_authenticated:
            self.fields['first_name'].initial = user.first_name or ''
            self.fields['last_name'].initial = user.last_name or ''
            self.fields['email'].initial = user.email or ''
