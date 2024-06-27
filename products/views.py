from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse
from .models import Category, Product
# from .models import Cart, CartItem
from core.models import SiteSettings
from django.contrib import messages

def product_list(request):
    site_settings = SiteSettings.objects.first()
    categories = Category.objects.all()
    products = Product.objects.all().order_by('?')
    user = request.user  # Retrieve the current logged-in user
    
    try:
        featured_category = Category.objects.get(name='Featured')
        featured_products = Product.objects.filter(category=featured_category)
    except Category.DoesNotExist:
        featured_products = Product.objects.none()
    
    context = {
        'site_settings': site_settings,
        'categories': categories,
        'products': products,
        'username': user.username,
        'f_pro': featured_products,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
    site_settings = SiteSettings.objects.first()
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:5]  # Limit to 5 related products for example

    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'site_settings': site_settings,
    })

def user_logout(request):
    logout(request)
    return redirect(reverse('login'))