from django.db.models import Count
from django.shortcuts import render,HttpResponse,redirect
from riyasapp.models import Product, Customer, Cart, Payment, OrderPlaced
from django.views import View
from .form import CustomerProfileForm
from django.contrib import messages
from math import ceil
from django.contrib import messages
from django.conf import settings
import razorpay 


# Create your views here.
def home(request):
    current_user = request.user
    print(current_user)
    allProds = []
    catProds = Product.objects.values('category','id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n=len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        allProds.append([prod, range(1,nSlides),nSlides])
    params = {'allProds':allProds}
    return render(request, 'index.html', params)


def product(request, pname): # pname == model(sub_category)
    if(Product.objects.filter(id=pname)):
        product=Product.objects.filter(id=pname).first()
        return render(request, 'product/product.html', {'product':product})
    else:
        messages.warning(request,"No such Catagory found")
        return redirect('/')
    
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'profile/profile.html', locals())
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, locality=locality, city=city, mobile=mobile, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! You have successfully")
        else:
            messages.success(request,"Invalid Input Data")
        # return render(request, 'product/profile.html', locals())
        return redirect('/profile')
    
def address(request):
    add = Customer.objects.filter(user = request.user)
    return render(request, 'profile/address.html', locals())

class updateaddress(View):
    def get(self,request,pk ):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'profile/updateaddress.html', locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations! Profile Update Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect('/address')
    

def addtocart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user = user, product = product).save()
    return redirect('/cart')

def cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.price
        amount += value
    totalamount = amount + 40   
    return render(request, 'product/addtocart.html', locals())

def removecart(request, pk):
    c = Cart.objects.get(id=pk)
    c.delete()
    return redirect('/cart')

class checkout(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        amount = 0
        for p in cart_items:
            values = p.quantity * p.product.price
            amount += values
        totalamount = amount+40
        razoramount = int(totalamount*100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount":razoramount, "currency":"INR", "receipt":"order_rcptid_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user = user,
                amount = totalamount,
                razorpay_order_id = order_id,
                razorpay_payment_status = order_status,
            )
            payment.save()
        pay = Payment.objects.get(razorpay_order_id = order_id)
        add1 = Customer.objects.get(user = user)
        return render(request, 'payment/checkout.html', locals())

def paymentdone(request):
    order_id = request.GET.get('order_id')
    # payment_id = request.GET.get('payment_id')
    razorpay_payment_id = request.POST.get("razorpay_payment_id")
    cust_id = request.GET.get('custid')
    user = request.user
    # print(cust_id)
    payment = Payment.objects.get(razorpay_order_id = order_id)
    # customer = Customer.objects.get(id=14)
    customer = Customer.objects.get(id=cust_id)
    payment.paid = True
    # payment.razorpay_payment_id = razorpay_payment_id
    payment.save()
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('orders')

def orders(request):
    return redirect('/')
