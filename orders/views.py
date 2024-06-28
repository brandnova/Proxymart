import json
import logging
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Order, OrderItem, Transaction, Product
from .paystack import initialize_payment, verify_payment
from cart.models import Cart, CartItem
from products.models import Product

def create_order(request):
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user)
        order = Order.objects.create(user=request.user, status='pending')
        
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        
        # Clear the cart after creating the order
        cart.items.all().delete()
        
        # Initialize payment
        try:
            authorization_url, reference = initialize_payment(request.user.email, order.get_total_price())
            # Create a transaction record
            Transaction.objects.create(order=order, transaction_id=reference, amount=order.get_total_price(), status='pending')
            return redirect(authorization_url)
        except Exception as e:
            # Handle initialization error (e.g., show an error message)
            return render(request, 'orders/payment_error.html', {'error': str(e)})
    
    return redirect('cart:checkout')


logger = logging.getLogger(__name__)

def payment_callback(request):
    reference = request.GET.get('reference')
    if reference is None:
        return JsonResponse({'error': 'No reference provided'}, status=400)

    try:
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }
        response = requests.get(f'{settings.PAYSTACK_BASE_URL}/transaction/verify/{reference}', headers=headers)
        response_data = response.json()

        if response.status_code == 200 and response_data['status']:
            transaction_data = response_data['data']
            transaction = get_object_or_404(Transaction, transaction_id=reference)
            order = transaction.order

            if transaction_data['status'] == 'success':
                transaction.status = 'completed'
                order.status = 'completed'
            else:
                transaction.status = 'failed'
                order.status = 'canceled'

            transaction.save()
            order.save()

            return redirect('orders:order_success', order_id=order.id)

        else:
            return JsonResponse({'error': 'Payment verification failed'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def paystack_webhook(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        event = payload.get('event')
        data = payload.get('data')
        
        if event == 'charge.success':
            reference = data.get('reference')
            try:
                payment_data = verify_payment(reference)
                transaction = Transaction.objects.get(transaction_id=reference)
                
                if payment_data['status'] == 'success':
                    transaction.status = 'completed'
                    transaction.save()
                    transaction.order.status = 'completed'
                    transaction.order.save()
                else:
                    transaction.status = 'failed'
                    transaction.save()
                    
                return JsonResponse({'status': 'success'}, status=200)
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        
        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'status': 'error'}, status=400)

def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # Create an order
        order = Order.objects.create(user=request.user, total_price=product.price)
        
        # Add the product to the order (assuming a single item order)
        order.items.create(product=product, quantity=1)

        # Create a transaction and initiate payment
        try:
            authorization_url, reference = initialize_payment(request.user.email, product.price)
            
            # Save the transaction
            transaction = Transaction.objects.create(
                user=request.user,
                order=order,
                transaction_id=reference,
                amount=product.price,
                status='pending'
            )

            return redirect(authorization_url)
        except Exception as e:
            return render(request, 'orders/payment_error.html', {'error': str(e)})

    return render(request, 'orders/buy_now.html', {'product': product})


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_success.html', {'order': order})


def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # Create an order
        order = Order.objects.create(user=request.user)

        # Add the product to the order
        order_item = OrderItem.objects.create(order=order, product=product, quantity=1, price=product.price)

        # Create a transaction and initiate payment
        try:
            authorization_url, reference = initialize_payment(request.user.email, order_item.get_total_price())
            
            # Save the transaction without the user argument
            transaction = Transaction.objects.create(
                order=order,
                transaction_id=reference,
                amount=order_item.get_total_price(),
                status='pending'
            )

            return redirect(authorization_url)
        except Exception as e:
            return render(request, 'orders/payment_error.html', {'error': str(e)})

    return render(request, 'orders/buy_now.html', {'product': product})
