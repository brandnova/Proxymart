from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.urls import reverse
from .models import SiteSettings
from products.models import Category, Product

# Create your views here.

def index(request):
    site_settings = SiteSettings.objects.first()
    categories = Category.objects.all()
    products = Product.objects.all().order_by('?')
    user = request.user
    username = user.username
    
    
    context = {
        'site_settings': site_settings,
        'categories': categories,
        'products': products,
        'user': user,
        'username': username,
    }
    return render(request, 'core/index.html', context)

def user_logout(request):
    logout(request)
    return redirect(reverse('login'))
