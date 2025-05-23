from django.urls import path
from .views import create_order, order_list

urlpatterns = [
    path('create/', create_order, name='create_order'),
    path('', order_list, name='order_list'),
]


