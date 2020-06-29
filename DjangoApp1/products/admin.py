from django.contrib import admin
from products.models import Products,OrderItem,Order,BookImage
admin.site.register(Products)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(BookImage)
# Register your models here.
