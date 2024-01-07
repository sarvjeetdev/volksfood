from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm


from .models import Food


def login_user(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            user_sess = {'user_name':user.username,'user_email':user.email}
            request.session['user'] = user_sess
            login(request, user)
            return redirect('home')
        else:
            return redirect("/")

    else:
        return render(request, 'login.html',{})

def home(request):
    query = request.GET.get('q')
    if query:
        foods = Food.objects.filter(name__icontains=query)
    else:
        foods = Food.objects.all()
    #return render(request, 'food_search.html', {'foods': foods, 'query': query})
    #foods = Food.objects.all()
    return render(request, 'home.html', {'foods': foods,'query': query})




class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class MyLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

class MyLogoutView(LogoutView):
    next_page = '/'





from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .models import Food,Order,OrderItem,Contact
from django.utils import timezone



@login_required(login_url="/users/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Food.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Food.objects.get(id=id)
    cart.remove(product)
    return redirect("home")


@login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Food.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Food.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("home")


@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("home")


@login_required(login_url="/users/login")
def cart_detail(request):
    return render(request, 'home.html')



import re

@login_required
def checkout(request):
    cart = Cart(request)
    #print("Ye rha caryttttttt",cart)
    total_amt=0 
    items = []
    for id,item in request.session['cart'].items():
        items.append(item)
        #print("\n\n",item)
        total_amt+= int(item['quantity'])*float(item['price'])
    contact = Contact.objects.filter(user=request.user).first()
    order = Order.objects.create(user=request.user, total_price=total_amt,date = timezone.now(),contact=contact)
    # Add cart items to the order
    for cart_item in items:
        #print("\n\nThis is CARTTTTTT ITEMMMMMMMMM\n\n",cart_item)
        order_item = OrderItem.objects.create(
            orderid=order,
            food_name=cart_item['name'],
            quantity=cart_item['quantity'],
            total=cart_item['price'],
            
            status = "Placed"
            
        )
        
    # Add cart items to the order
    # Clear the cart after checkout
    cart.clear()
    # Pass order details to the template
    return render(request, 'checkout.html', {'order': order})


from collections import defaultdict
@login_required
def order_history(request):
    # Retrieve all orders for the logged-in user
    orders = Order.objects.filter(user=request.user)
    
    # Retrieve order items for each order
    order_items = defaultdict(list)
    for order in orders:
        items = OrderItem.objects.filter(orderid=order.orderid)
        x  = items.values_list('status','food_name','quantity','total')
        #print("ITEMSSS ARE",x)
        
        for i in range(len(x)):
            d = dict()
            #print(i,x[i])
            d['status']=x[i][0]
            d['name']=x[i][1]
            d['quantity']=x[i][2]
            d['total']=x[i][3]
            order_items[order.orderid].append(d)
        #print(order_items)
    context = []
    for order in orders:
        context.append((order, order_items.get(order.orderid, [])))

    #print("\n\nCONTEXT",context)
    #print("\n\n")
    return render(request, 'orders.html', {'context': context})

from .forms import ContactForm
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            #print(request)

            delivery_details = form.save(commit=False)
            #order = Order.objects.filter(user=request.user)
            #print("\nOrderr", order)
            #print()
            delivery_details.user = request.user
            #delivery_details.orderid = order
            delivery_details.save()
            return redirect('checkout') 
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})




from .models import Food

def food_search(request):
    query = request.GET.get('q')
    if query:
        foods = Food.objects.filter(name__icontains=query)
    else:
        foods = Food.objects.all()
    return render(request, 'food_search.html', {'foods': foods, 'query': query})