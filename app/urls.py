from django.urls import path
from app import views
urlpatterns = [
    path('', views.home,name="home"),
    path('product-detail/<str:slug>/', views.product_detail, name='product-detail'),
    path('cart/', views.order_summary, name='order_summary'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.profile, name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('changepassword/', views.change_password, name='changepassword'),
    path('mobile/', views.mobile, name='mobile'),
    path('login/', views.login, name='login'),
    path('registration/', views.customerregistration, name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path("add_to_cart/<str:slug>/",views.add_to_cart,name="add_to_cart"),
    path("remove_from_cart/<str:slug>/",views.remove_from_cart,name="remove_from_cart"),
    path("minimize_quantity/<str:slug>/",views.minimize_quantity,name="minimize_quantity"),
    path("logout/",views.logout,name="logout"), 
]
