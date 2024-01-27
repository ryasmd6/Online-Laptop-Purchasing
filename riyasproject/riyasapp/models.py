from django.db import models
from django.contrib.auth.models import User
# Create your models here.

STATE_CHOICES = (
   ("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry"),
)

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the way','On the way'),
    ('Delivered','Delivered'),
    ('Cancelled','Cancelled'),
    ('Pending','Pending'),
)

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default="")
    sub_category = models.CharField(max_length=500, default="")
    price = models.IntegerField(default=0)
    mrp = models.IntegerField(default=0)
    des1 = models.CharField(max_length=300, default="")
    des2 = models.CharField(max_length=300, default="")
    des3 = models.CharField(max_length=300, default="")
    des4 = models.CharField(max_length=300, default="")
    des5 = models.CharField(max_length=300, default="") #description
    pub_date = models.DateField()   #published date
    image1 = models.ImageField(upload_to='shop/images/', default="")
    image2 = models.ImageField(upload_to='shop/images/', default="")
    image3 = models.ImageField(upload_to='shop/images/', default="")
    image4 = models.ImageField(upload_to='shop/images/', default="")
    image5 = models.ImageField(upload_to='shop/images/', default="")
    def __str__(self):
        return self.product_name

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=300)
    city = models.CharField(max_length=300)
    mobile = models.CharField(max_length=10)
    zipcode = models.IntegerField(default=0)
    state = models.CharField(choices=STATE_CHOICES, max_length=255, null=True, blank=True)
def __str__(self):
    return self.name


class Cart(models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.qunatity * self.product.price

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_payment_status = models.CharField(max_length=200, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True)
    paid = models.BooleanField(default=False)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity =  models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices = STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default="")

    @property
    def total_cost(self):
        return self.quantity * self.product.price