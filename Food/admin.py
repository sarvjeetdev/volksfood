from django.contrib import admin

# Register your models here.
from .models import Category, Food, Order, Profile,Cart,CartItem,OrderItem,Contact
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin




admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Food)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderItem)
admin.site.register(Contact)
