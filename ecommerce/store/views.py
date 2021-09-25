from django.shortcuts import redirect, render

from django.http import JsonResponse
from .models import *

import json
import datetime

from .utils import cookieCart, cartData, guestOrder
# Create your views here.


def store(request):

    data = cartData(request)
    cartItems = data['cartItems']


    products = Product.objects.all()

    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']


    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']


    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)


def removeitem(request):
    data = json.loads(request.body)
    productId = data['productId']

    print('productId:', productId)

    order = Order.objects.get(complete=False)

    OrderItem.objects.filter(product__id = productId, order = order).delete()
    
    num_items = order.get_cart_items
    total = order.get_cart_total

    data = {'items':num_items, 'total':total}
    return JsonResponse(data, safe=False)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()


    num_items = order.get_cart_items
    return JsonResponse(num_items, safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)


    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )

    return JsonResponse('Payment complete!', safe=False)
