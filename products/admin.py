from django.contrib import admin
from .models import Category, Product
# from .models import Cart, CartItem
from .forms import ProductForm

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ('name', 'category', 'price', 'quantity')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'images', 'quantity', 'category', 'specifications')
        }),
    )

# admin.site.register(Cart)
# admin.site.register(CartItem)