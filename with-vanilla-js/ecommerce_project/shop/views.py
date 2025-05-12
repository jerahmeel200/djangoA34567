from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Product, Cart, CartItem
from .serializers import ProductSerializer, CartSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartviewSet(viewsets.ViewSet):
    def create(self, request):
        cart = Cart.objects.create()
        return Response({"cart_id": cart.id}, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        try:
            cart = Cart.objects.get(pk=pk)
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)  
        
        
    
    @action(detail=True, methods=["post"])
    def add_item(self, request, pk=None):
        cart = Cart.objects.get(pk=pk)
        product_id = request.data['product_id']
        quantity = int(request.data.get('quantity', 1))
        product = Product.objects.get(pk=product_id)  
        
        
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()
        return Response({"status": "item added"})
    
    
    @action(detail=True, methods=["post"])
    def remove_item(self, request, pk=None):
        cart = Cart.objects.get(pk=pk)
        product_id = request.data['product_id']
        CartItem.objects.filter(cart=cart, product_id=product_id).delete()
        return Response({"status": "item removed"})    


 
