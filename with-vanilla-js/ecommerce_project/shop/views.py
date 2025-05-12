from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Product, Cart, CartItem
from .serializers import ProductSerializer, CartSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartViewSet(viewsets.ViewSet):  # ✅ Fixed class name capitalization
    def create(self, request):
        cart = Cart.objects.create()
        return Response({"cart_id": cart.id}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        cart = get_object_or_404(Cart, pk=pk)  # ✅ Uses get_object_or_404
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def add_item(self, request, pk=None):
        cart = get_object_or_404(Cart, pk=pk)

        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        if not product_id:
            return Response(
                {"error": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            quantity = int(quantity)
            if quantity < 1:
                raise ValueError()
        except (ValueError, TypeError):
            return Response(
                {"error": "Quantity must be a positive integer"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        product = get_object_or_404(Product, pk=product_id)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()

        serializer = CartSerializer(cart)
        return Response(
            {"status": "item added", "cart": serializer.data},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def remove_item(self, request, pk=None):
        cart = get_object_or_404(Cart, pk=pk)

        product_id = request.data.get("product_id")
        if not product_id:
            return Response(
                {"error": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        CartItem.objects.filter(cart=cart, product_id=product_id).delete()

        serializer = CartSerializer(cart)
        return Response(
            {"status": "item removed", "cart": serializer.data},
            status=status.HTTP_200_OK,
        )
