from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.paginator import Paginator

from .models import *
from .forms import  OrderForm,CreateUserForm
from .filters import OrderFilter
from .decorators import unauthenticated_user,allowed_users,admin_only




# Create your views here.
@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()
    if request.method=='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
                name=user.username,
                )

            messages.success(request,'Account was created for '+ username)
            return redirect('login')

    context = {'form':form}
    return render(request,'accounts/register.html',context)


@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        
        username = request.POST.get('username')
        password =  request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'username or password is incorrect')
    context = {}
    return render(request,'accounts/login.html',context)


def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
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


@login_required(login_url='login')
def products(request):
    ps = Product.objects.all()
    
    paginator = Paginator(ps, 3) # Show 3 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    context = {'ps': page_obj}
    return render(request,'accounts/products.html',context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_order = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pinding  = orders.filter(status='Pending').count()
    
    context = {
        'orders' :orders,
        'total_order':total_order,
        'delivered':delivered,
        'pinding':pinding,
        }
    return render(request,'accounts/user.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    
    context={'item':order}
    return render(request,'accounts/delete.html',context)