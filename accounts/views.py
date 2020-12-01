from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm

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


def customer(request,pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    orders_count = orders.count()

    context = {
        'customer':customer,
        'orders':orders,
        'orders_count':orders_count,
        }

    return render(request,'accounts/customer.html', context)


def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields='product,ststus')
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(instance=customer)
    #form = OrderForm(initial={'customer':customer})
    
    if request.method=="POST":
        form=OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':formset}
    return render(request,'accounts/order_form.html',context)

def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method=="POST":
            form=OrderForm(request.POST,instance=order)
            if form.is_valid():
                form.save()
                return redirect('/')

    context = {'form':form}
    return render(request,'accounts/order_form.html',context)

def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    
    context={'item':order}
    return render(request,'accounts/delete.html',context)