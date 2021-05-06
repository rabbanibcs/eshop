from django.db import models


class Product(models.Model):
    code=models.PositiveIntegerField(max_length=10)
    name=models.CharField(max_length=100)
    description=models.TextField()
    image=models.ImageField(blank=True,default='default.png')
    category=models.ForeignKey('Customer',on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=9,decimal_places=2)
    stock=models.IntegerField(max_length=10)

    def __str__(self):
        return self.name


class Category(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True) #
    quantity=models.IntegerField(default=0,null=True,blank=True)
    complete=models.BooleanField(default=False)

class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    date_added=models.DateField(auto_now_add=True)
    address=models.TextField()
    product_name=models.CharField(max_length=100)
    quantity=models.IntegerField(default=0,null=True,blank=True)



    def __str__(self):
        return str(self.id)