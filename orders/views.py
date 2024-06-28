import json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderItem, Transaction
from .paystack import initialize_payment, verify_payment
from cart.models import Cart, CartItem

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

def payment_callback(request):
    reference = request.GET.get('reference')
    try:
        payment_data = verify_payment(reference)
        transaction = Transaction.objects.get(transaction_id=reference)
        
        if payment_data['status'] == 'success':
            transaction.status = 'completed'
            transaction.save()
            transaction.order.status = 'completed'
            transaction.order.save()
            # Redirect to a success page or display a success message
            return redirect('order_success', order_id=transaction.order.id)
        else:
            # Handle payment verification failure
            transaction.status = 'failed'
            transaction.save()
            return render(request, 'orders/payment_error.html', {'error': 'Payment verification failed.'})
    
    except Exception as e:
        # Handle verification error
        return render(request, 'orders/payment_error.html', {'error': str(e)})

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