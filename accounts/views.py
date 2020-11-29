from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_order = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pinding  = orders.filter(status='Pending').count()


    context = {
        'orders' :orders,
        'customers' :customers, 
        'total_customers':total_customers,
        'total_order':total_order,
        'delivered':delivered,
        'pinding':pinding,
        }

    
    return render(request,'accounts/dashboard.html', context)

def homee(request):
    ps = Product.objects.all()
    context = {'ps': ps}
    return render(request,'accounts/homee.html',context)

def products(request):
    ps = Product.objects.all()
    context = {'ps': ps}
    return render(request,'accounts/products.html',context)


def customer(request):
    return render(request,'accounts/customer.html')

