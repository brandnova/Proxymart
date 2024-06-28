import requests
from django.conf import settings

PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
PAYSTACK_BASE_URL = 'https://api.paystack.co'

def initialize_payment(email, amount):
    headers = {
        'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json',
    }
    data = {
        "email": email,
        "amount": int(amount * 100),  # Paystack expects the amount in kobo
    }
    response = requests.post(f'{PAYSTACK_BASE_URL}/transaction/initialize', headers=headers, json=data)
    response_data = response.json()
    if response.status_code == 200 and response_data['status']:
        return response_data['data']['authorization_url'], response_data['data']['reference']
    else:
        raise Exception(f"Failed to initialize payment: {response_data.get('message')}")

def verify_payment(reference):
    headers = {
        'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}',
    }
    response = requests.get(f'{PAYSTACK_BASE_URL}/transaction/verify/{reference}', headers=headers)
    response_data = response.json()
    if response.status_code == 200 and response_data['status']:
        return response_data['data']
    else:
        raise Exception(f"Failed to verify payment: {response_data.get('message')}")
