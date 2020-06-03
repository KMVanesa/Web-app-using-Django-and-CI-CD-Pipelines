from django.contrib import admin
from products.models import Products,OrderItem,Order
admin.site.register(Products)
admin.site.register(OrderItem)
admin.site.register(Order)
# Register your models here.
