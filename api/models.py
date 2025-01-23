from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)


class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField()
    quantity = models.IntegerField()


class Order(models.Model):
    id_customer = models.ForeignKey(to=Customer, related_name='customer', on_delete=models.CASCADE)
    date = models.DateField()
    total = models.FloatField()


class OrderItems(models.Model):
    id_order = models.ForeignKey(to=Order, related_name='order_items', on_delete=models.CASCADE)
    id_product = models.ForeignKey(to=Product, related_name='product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
