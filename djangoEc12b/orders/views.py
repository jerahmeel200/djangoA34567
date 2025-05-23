from django.shortcuts import render, redirect
from .models import Order, OrderItem
from cart.cart import Cart
from django.contrib.auth.decorators import login_required



@login_required
def create_order(request):
    cart = Cart(request)
    order = Order.objects.create(user=request.user)
    for item in cart:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            price=item['product'].price,
            quantity=item['quantity']
        )
    cart.clear()
    return redirect('order_list')  

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders}) 
