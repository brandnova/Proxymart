from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create_order/', views.create_order, name='create_order'),
    path('initialize_payment/<int:order_id>/', views.initialize_payment, name='initialize_payment'),
    path('payment_callback/', views.payment_callback, name='payment_callback'),
    path('webhook/', views.paystack_webhook, name='paystack_webhook'),
]