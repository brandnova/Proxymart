from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse
from products.models import Product, Category
from .forms import AdditionalOrderInfoForm
from orders.views import create_order
from .models import Cart, CartItem
from core.models import SiteSettings
from accounts.models import Profile

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
    user = request.user
    products = Product.objects.all()
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile(user=user) 

    site_settings = SiteSettings.objects.first()
    cart, created = Cart.objects.get_or_create(user=request.user)
    total_price = cart.get_total_price()
    categories = Category.objects.all()
    return render(request, 'cart/cart_detail.html', {
        'products': products,
        'cart': cart, 
        'profile': profile, 
        'total_price': total_price,
        'categories': categories,
        'site_settings': site_settings,
        })

def user_logout(request):
    logout(request)
    return redirect(reverse('login'))

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    site_settings = SiteSettings.objects.first()

    if request.method == 'POST':
        form = AdditionalOrderInfoForm(request.POST)
        if form.is_valid():
            # If form is valid, proceed to create the order
            return create_order(request, form.cleaned_data)
    else:
        form = AdditionalOrderInfoForm()

    return render(request, 'cart/checkout.html', {
        'cart': cart,
        'site_settings': site_settings,
        'form': form,
    })


