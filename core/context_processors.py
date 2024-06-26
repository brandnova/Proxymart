from products.models import Category
from .models import SiteSettings


def categories(request):
    return {
        'categories': Category.objects.all()
    }
# core/context_processors.py


def site_settings(request):
    try:
        settings = SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        settings = None
    return {'site_settings': settings}

# core/context_processors.py

# def cart_count(request):
#     if request.user.is_authenticated:
#         cart = Cart.objects.filter(user=request.user).first()
#     else:
#         cart_id = request.session.get('cart_id')
#         cart = Cart.objects.filter(id=cart_id).first() if cart_id else None

#     count = CartItem.objects.filter(cart=cart).count() if cart else 0
#     return {'cart_count': count}

