from django.contrib import admin
from StyleVaneApp.models import Products, Blogs, CartItem, Order, OrderDetail

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_image','product_title','product_des','product_price')

admin.site.register(Products,ProductAdmin)

class BlogAdmin(admin.ModelAdmin):
    list_display = ('blog_image','blog_title','blog_des')

admin.site.register(Blogs,BlogAdmin)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user','product','quantity')

admin.site.register(CartItem,CartItemAdmin)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_date', 'total')
    list_filter = ('order_date',)

@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'subtotal')
    list_filter = ('order__order_date', 'product')
