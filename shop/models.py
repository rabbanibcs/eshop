from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    code = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    image = models.ImageField(blank=True, default='default.png')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True,blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.name




class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)  #
    quantity = models.IntegerField(default=0, null=True, blank=True)
    complete = models.BooleanField(default=False)


class Order(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.IntegerField()
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return self.name
