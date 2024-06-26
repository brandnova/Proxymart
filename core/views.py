from django.shortcuts import render
from .models import SiteSettings
from products.models import Category, Product

# Create your views here.

def index(request):
    site_settings = SiteSettings.objects.first()
    categories = Category.objects.all()
    products = Product.objects.all().order_by('?')
    user = request.user
    username = user.username
    
    # if request.user.is_authenticated:
    #     cart_count = CartItem.objects.filter(user=request.user).count()
    # else:
    #     cart_count = 0
    context = {
        'site_settings': site_settings,
        'categories': categories,
        'products': products,
        # 'cart_count': cart_count,
        'user': user,
        'username': username,
    }
    return render(request, 'core/index.html', context)


