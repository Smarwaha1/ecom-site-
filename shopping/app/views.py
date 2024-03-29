from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, OrderPlaced, Cart
from .forms import CustomerRegistrationForm, CustomerProfileForm

class ProductView(View):

 def get(self, request):
  topwears = Product.objects.filter(category='TW')
  bottomwears = Product.objects.filter(category='BW')
  mobiles = Product.objects.filter(category='M')
  laptops = Product.objects.filter(category='L')
  return render(request, 'app/home.html',
                {'topwears': topwears, 'bottomwears': bottomwears, 'mobiles': mobiles, 'laptops': laptops})


class ProductDetailView(View):
 def get(self, request, pk):
  """
  we will be writing detail view over here to get the deatils of the product
  """
  product = Product.objects.get(pk=pk)
  print(product.id)
  return render(request, 'app/productdetail.html', {'product':product})


def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id') # to get the product id
 # we need to get the instance of the product id that can be acheived by
 product = Product.objects.get(id=product_id)
 Cart(user=user, product=product).save() # saving the product in cart
 return redirect('/cart')


def show_cart(request):
 if request.user.is_authenticated:
  user = request.user
  cart=Cart.objects.filter(user=user)
  # print(cart)
  amount = 0.0
  shipping_amount =70.0
  total_amount = 0.0
  cart_product =[p for p in Cart.objects.all() if p.user==user]
  # print(cart_product)
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
    total_amount = amount + shipping_amount
    return render(request, 'app/addtocart.html', {'carts': cart, 'totalamount': total_amount, 'amount': amount})
  else:
   return render(request, 'app/emptycart.html')

def plus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity += 1
  c.save()
  amount = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   tempamount = (p.quantity * p.product.discounted_price)
   # print("Quantity", p.quantity)
   # print("Selling Price", p.product.discounted_price)
   # print("Before", amount)
   amount += tempamount
   # print("After", amount)
   # print("Total", amount)
  data = {
   'quantity': c.quantity,
   'amount': amount,
   'totalamount': amount + shipping_amount
  }
  return JsonResponse(data)
 else:
  return HttpResponse("")


def minus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity -= 1
  c.save()
  amount = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   tempamount = (p.quantity * p.product.discounted_price)
   # print("Quantity", p.quantity)
   # print("Selling Price", p.product.discounted_price)
   # print("Before", amount)
   amount += tempamount
  # print("After", amount)
  # print("Total", amount)
  data = {
   'quantity': c.quantity,
   'amount': amount,
   'totalamount': amount + shipping_amount
  }
  return JsonResponse(data)
 else:
  return HttpResponse("")


def remove_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.delete()
  amount = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   tempamount = (p.quantity * p.product.discounted_price)
   # print("Quantity", p.quantity)
   # print("Selling Price", p.product.discounted_price)
   # print("Before", amount)
   amount += tempamount
  # print("After", amount)
  # print("Total", amount)
  data = {
   'amount': amount,
   'totalamount': amount + shipping_amount
  }
  return JsonResponse(data)
 else:
  return HttpResponse("")


def buy_now(request):
 return render(request, 'app/buynow.html')


def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary'})

def orders(request):
 op = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html', {'order_placed':op})

def mobile(request, data=None):
 if data == None:
  mobiles = Product.objects.filter(category='M')
 elif data == 'Apple' or data =='Samsung':
  mobiles = Product.objects.filter(category='M').filter(brand=data)
 elif data == 'below':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=50000)
 elif data == 'above':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=50000)
 return render(request, 'app/mobile.html', {'mobiles':mobiles})

def topwear(request, data=None):
 if data == None:
  topwears = Product.objects.filter(category='TW')
 elif data == 'hell' or data =='Sau':
  topwears = Product.objects.filter(category='TW').filter(brand=data)
 elif data == 'below':
  topwears = Product.objects.filter(category='TW').filter(discounted_price__lte=450)
 elif data == 'above':
  topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=450)
 return render(request, 'app/topwear.html', {'topwears':topwears})

def bottomwear(request, data=None):
 if data == None:
  bottomwears = Product.objects.filter(category='BW')
 elif data == 'levis' or data =='hell' or data =='spykar' or data == 'lee':
  bottomwears = Product.objects.filter(category='BW').filter(brand=data)
 elif data == 'below':
  bottomwears = Product.objects.filter(category='BW').filter(discounted_price__lte=560)
 elif data == 'above':
  bottomwears = Product.objects.filter(category='BW').filter(discounted_price__gt=560)
 return render(request, 'app/bottomwear.html', {'bottomwears':bottomwears})



class CustomerRegistrationView(View):
 def get(self, request):
  form = CustomerRegistrationForm()
  return render(request, 'app/customerregistration.html', {'form': form})

 def post(self, request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulations!! Registered Successfully.')
   form.save()
  return render(request, 'app/customerregistration.html', {'form': form})

def checkout(request):
 user = request.user
 add = Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=request.user)
 amount = 0.0
 shipping_amount = 70.0
 totalamount = 0.0
 cart_product = [p for p in Cart.objects.all() if p.user == request.user]
 if cart_product:
  for p in cart_product:
   tempamount = (p.quantity * p.product.discounted_price)
   amount += tempamount
  totalamount = amount + shipping_amount
 return render(request, 'app/checkout.html', {'add': add, 'cart_items': cart_items, 'totalcost': totalamount})

def payment_done(request):
 custid = request.GET.get('custid')
 print("Customer ID", custid)
 user = request.user
 cartid = Cart.objects.filter(user=user)
 customer = Customer.objects.get(id=custid)
 print(customer)
 for cid in cartid:
  OrderPlaced(user=user, customer=customer, product=cid.product, quantity=cid.quantity).save()
  print("Order Saved")
  cid.delete()
  print("Cart Item Deleted")
 return redirect("orders")



class ProfileView(View):
 def get(self, request):
  form = CustomerProfileForm()
  return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})

 def post(self, request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   usr = request.user
   name = form.cleaned_data['name']
   locality = form.cleaned_data['locality']
   city = form.cleaned_data['city']
   state = form.cleaned_data['state']
   zipcode = form.cleaned_data['zipcode']
   reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
   reg.save()
   messages.success(request, "Congratulations!!, Profile updated successfully")
  return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})



