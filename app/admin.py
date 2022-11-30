from django.contrib import admin
from .models import Product,Payment,Order,Cart,Address

# Register your models here.

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Address)
admin.site.register(Payment)
admin.site.register(Order)