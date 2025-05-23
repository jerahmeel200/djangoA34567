def cart_context(request):
    from .cart import Cart
    return {'cart': Cart(request)}
