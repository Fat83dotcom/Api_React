from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=128)
    second_name = models.CharField(max_length=128, default='')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.category_name}'


class ProductCategory(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.category_name}'


class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField()
    quantity = models.IntegerField()
    category = models.ForeignKey(
        to=ProductCategory, on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return f'{self.category_name}'


class Order(models.Model):
    id_customer = models.ForeignKey(
        to=Customer, related_name='customer', on_delete=models.CASCADE
    )
    date = models.DateField()
    total = models.FloatField()
    order_status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.category_name}'


class OrderItems(models.Model):
    id_order = models.ForeignKey(to=Order, related_name='order_items', on_delete=models.CASCADE)
    id_product = models.ForeignKey(to=Product, related_name='product', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.id_order}'
