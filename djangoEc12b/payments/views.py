from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
import requests


@login_required
def payment_process(request):
    cart = request.session.get('cart', {})
    total_amount = sum(float(item['price']) * item['quantity'] for item in cart.values()) * 100

    if request.method == 'POST':
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }
        data = {
            'email': request.user.email,
            'amount': int(total_amount),
        }
        response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, json=data)
        res_data = response.json()

        if res_data.get('status'):
            auth_url = res_data['data']['authorization_url']
            return redirect(auth_url)
        else:
            return render(request, 'payments/payment_failed.html', {'error': res_data.get('message')})
    return render(request, 'payments/payment_process.html', {'total_amount': total_amount})

