from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from products.models import Product, Category
from .models import Cart, CartItem
from core.models import SiteSettings

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart_detail')

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        cart_item.quantity = int(quantity)
        cart_item.save()
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    site_settings = SiteSettings.objects.first()
    cart, created = Cart.objects.get_or_create(user=request.user)
    total_price = cart.get_total_price()
    categories = Category.objects.all()
    return render(request, 'cart/cart_detail.html', {
        'cart': cart, 
        'total_price': total_price,
        'categories': categories,
        'site_settings': site_settings,
        })