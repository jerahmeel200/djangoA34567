class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart   
        
    
    def add(self, product, quantity=1):
            product_id  = str(product.id)
            if product_id not in self.cart:
                self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
            self.cart[product_id]['quantity'] += quantity 
            self.save()
            
    def save(self):
        self.session.modified = True           
            
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save() 
    
    def __iter__(self):
        from products.models import Product
        for product_id in self.cart.keys():
            product = Product.objects.get(id=product_id)
            item = self.cart[product_id]
            item['product'] = product
            item['total_price'] = float (item['price']) * item['quantity'] 
            yield item 
            
            
    def clear(self):
        self.session['cart'] = {}
        self.save()               