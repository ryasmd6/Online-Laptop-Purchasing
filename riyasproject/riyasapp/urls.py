from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    # path('product',views.product,name='product'),
    path('product/<str:pname>' ,views.product, name="product"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('address/', views.address, name="address"),
    path('updateaddress/<int:pk>/', views.updateaddress.as_view(), name="updateaddress"),
    path('addtocart/', views.addtocart, name="addtocart"),
    path('cart/', views.cart, name="cart"),
    path('removecart/<int:pk>/', views.removecart, name="removecart"),
    path('checkout/', views.checkout.as_view(), name='checkout'),
    path('paymentdone/', views.paymentdone, name='paymentdone'),
    path('orders/', views.orders, name='orders'),


]
