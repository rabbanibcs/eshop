from django.contrib import admin
from .models import Product,Category,Cart,Order,Customer

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','stock')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass