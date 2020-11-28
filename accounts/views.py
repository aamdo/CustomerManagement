from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    context = {'orders' :orders,'customers' :customers }
    
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

