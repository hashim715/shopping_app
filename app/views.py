from django.shortcuts import render,redirect
from .models import Product,Cart,Address,Order,Payment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def home(request):
   products=Product.objects.all()
   context={"products":products}
   return render(request, 'app/home.html',context=context)

def product_detail(request,slug=None):
   product=Product.objects.filter(slug=slug)
   checker=False
   if product.exists():
      return render(request, 'app/productdetail.html',context={"product":product[0]})
   else:
      return redirect("home")

@login_required(login_url="login")
def order_summary(request):
   total_amount=0
   total_objects=0
   cart_objects=Cart.objects.filter(user=request.user)
   for object in cart_objects:
      total_objects+=1
      if object.product.discount_price:
         total_amount+=object.product.discount_price*object.quantity
      else:
         total_amount+=object.product.price*object.quantity
   total_amount_including=total_amount+70
   return render(request, 'app/addtocart.html',context={"cart_objs":cart_objects,"total_amount":total_amount,"final_amount":total_amount_including})

def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required(login_url="login")
def profile(request):
   if request.method=='POST':
      name=request.POST.get('name')
      address=request.POST.get('address')
      address2=request.POST.get('address2')
      city=request.POST.get('city')
      state=request.POST.get('state')
      zip_code=request.POST.get('zip_code')
      check_address=Address.objects.filter(name=name)
      if check_address.exists():
         messages.warning(request,"Address with tha name already exists")
         return redirect("profile")
      address=Address.objects.create(name=name,address=address,
      city=city,state=state,zip_code=zip_code)
      address.save()
   return render(request, 'app/profile.html')

@login_required(login_url="login")
def address(request):
   address_objs=Address.objects.filter(user=request.user)
   context={"objs":[]}
   if address_objs.exists():
      context={"objs":address_objs}
   return render(request, 'app/address.html',context=context)

def orders(request):
 return render(request, 'app/orders.html')

@login_required(login_url="login")
def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request):
 return render(request, 'app/mobile.html')

def login(request):
   if request.method=='POST':
      username=request.POST.get('username')
      password=request.POST.get('password')
      user=authenticate(username=username,password=password)
      if user is not None:
         auth_login(request,user)
         return redirect("home")
      else:
         return redirect("home")
   return render(request, 'app/login.html')

def customerregistration(request):
   if request.method=='POST':
      email=request.POST.get('email')
      password=request.POST.get('password')
      username=request.POST.get('username')
      if len(email)>5 and len(password)>6:
         user_obj=User.objects.filter(email=email)
         if user_obj.exists():
            return render("home")
         else:
            user_create_obj=User.objects.create(username=username,email=email,password=password)
            user_create_obj.save()
            return redirect("login")
   return render(request, 'app/customerregistration.html')

@login_required(login_url="login")
def checkout(request):
   if request.method=='POST':
      credit_card_number=request.POST.get("credit_card")
      address=request.POST.get('address')
      address_obj=Address.objects.filter(name=address)
      cart_obj=Cart.objects.filter(user=request.user)
      check_payment_obj=Payment.objects.filter(user=request.user)
      if check_payment_obj.exists():
         payment_obj=check_payment_obj[0]
      else:
         payment_obj=Payment.objects.create(user=request.user,card_number=credit_card_number)
         payment_obj.save()
      if address_obj.exists():
         address_obj=address_obj[0]
      else:
         return redirect("checkout")
      cart_objects_array=[]
      for i in range(len(cart_obj)):
         cart_objects_array.append(cart_obj[i].product)
      order_obj=Order.objects.create(user=request.user,payment=payment_obj,address=address_obj)
      order_obj.products.set(cart_objects_array)
      order_obj.save()
      cart_obj.delete()
      return redirect("home")
   products=Cart.objects.filter(user=request.user)
   addresses=Address.objects.filter(user=request.user)
   product_array=[]
   context={"products":product_array,"addresses":addresses}
   if products.exists():
      for product in products:
         final_price=0
         if product.product.discount_price:
            final_price=product.product.discount_price*product.quantity
         else:
            final_price=product.product.price*product.quantity
         product_array.append({
            "title":product.product.title,
            "quantity":product.quantity,
            "price":product.product.price,
            "discount_price":product.product.discount_price,
            "final_price":final_price
         })
      context={"products":product_array,"addresses":addresses}
   else:
      return redirect("home")
   return render(request, 'app/checkout.html',context=context)

@login_required(login_url="login")
def add_to_cart(request,slug=None):
   product=Product.objects.filter(slug=slug)
   if product.exists():
      cart_check=Cart.objects.filter(user=request.user,product=product[0])
      if cart_check.exists():
         cart_check_obj=cart_check[0]
         cart_check_obj.quantity+=1
         cart_check_obj.save()
      else:
         cart_create_obj=Cart.objects.create(user=request.user,product=product[0],quantity=1)
         cart_create_obj.save()
      return redirect("order_summary")
   else:
      return redirect("home")

@login_required(login_url="login")
def remove_from_cart(request,slug=None):
   product=Product.objects.filter(slug=slug)
   if product.exists():
      cart_obj=Cart.objects.filter(product=product[0],user=request.user)
      if cart_obj.exists():
         cart_obj.delete()
      else:
         return redirect("order_summary")
      return redirect("order_summary")
   else:
      return redirect("home")

@login_required(login_url="login")
def minimize_quantity(request,slug=None):
   product=Product.objects.filter(slug=slug)
   if product.exists():
      cart_check=Cart.objects.filter(user=request.user,product=product[0])
      if cart_check.exists():
         cart_check_obj=cart_check[0]
         if cart_check_obj.quantity==1:
            cart_check_obj.delete()
            return redirect("order_summary")
         else:
            cart_check_obj.quantity-=1
            cart_check_obj.save()
         return redirect("order_summary")
      else:
         return redirect("home")
   else:
      return redirect("home")

@login_required(login_url="login")
def logout(request):
   auth_logout(request)
   return redirect("home")
