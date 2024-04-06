from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User

# Product model

class Products(models.Model):
    product_image = models.FileField(upload_to="product_images/",max_length=250,null=True,default=None)
    product_title = models.CharField(max_length=100)
    product_des = HTMLField()
    product_price = models.CharField(max_length=50)

class Blogs(models.Model):
    blog_image = models.FileField(upload_to="blog_images/",max_length=250,null=True,default=None)
    blog_title = models.CharField(max_length=100)
    blog_des = HTMLField()

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
