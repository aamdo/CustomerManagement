from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm
from .filters import OrderFilter
from django.core.paginator import Paginator

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
    
    paginator = Paginator(ps, 3) # Show 3 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    context = {'ps': page_obj}
    return render(request,'accounts/products.html',context)


def customer(request,pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    orders_count = orders.count()

    myFilter = OrderFilter(request.GET,queryset=orders)
    orders = myFilter.qs

    context = {
        'customer':customer,
        'orders':orders,
        'orders_count':orders_count,
        'myFilter':myFilter,
        }

    return render(request,'accounts/customer.html', context)


def createOrder(request, pk):

    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra=3)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
        
    if request.method=="POST":
        #form=OrderForm(request.POST)
        formset = OrderFormSet( request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset':formset}
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