from django.contrib import admin
from .models import Order, OrderItem, Transaction

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'order_ref', 'user', 'status', 'created_at', 'updated_at')  # Include 'order_ref' here
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'id')

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'order', 'amount', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('transaction_id', 'order__id')

admin.site.register(Order, OrderAdmin)
admin.site.register(Transaction, TransactionAdmin)
