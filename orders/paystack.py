import requests
from django.conf import settings

PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
PAYSTACK_BASE_URL = 'https://api.paystack.co'

def initialize_payment(email, amount):
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',  # Assuming PAYSTACK_SECRET_KEY is in your settings
        'Content-Type': 'application/json',
    }
    data = {
        "email": email,
        "amount": int(amount * 100),  # Paystack expects the amount in kobo
    }
    response = requests.post(f'{settings.PAYSTACK_BASE_URL}/transaction/initialize', headers=headers, json=data)
    response_data = response.json()
    
    if response.status_code == 200 and response_data['status']:
        return response_data['data']['authorization_url'], response_data['data']['reference']
    else:
        error_message = response_data.get('message', 'An error occurred while initializing payment.')
        raise Exception(f"Failed to initialize payment: {error_message}")

def verify_payment(reference):
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
    }
    response = requests.get(f'https://api.paystack.co/transaction/verify/{reference}', headers=headers)
    response_data = response.json()
    if response.status_code == 200 and response_data['status']:
        return response_data['data']
    else:
        raise Exception('Failed to verify payment')