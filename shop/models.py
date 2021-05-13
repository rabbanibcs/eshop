from django.db import models
import qrcode

# all category
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# products table
class Product(models.Model):
    code = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    image = models.ImageField(blank=True, default='default.png')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.name

# all orders give by customers
class Order(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

# all products in a given order
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)  #
    quantity = models.IntegerField(default=0, null=True, blank=True)
    complete = models.BooleanField(default=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product.name)
# customer detail
class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.IntegerField()
    email = models.EmailField()
    qrcode = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
# QR code generate and return the path of the qr code
    def qrcode_create(self):
        image = qrcode.make('name: ' + self.name + '\nphone: ' + self.phone + '\nemail: ' + self.email)
        path = 'media/' + str(self.id) + self.name + '.png'
        image.save(path)
        path = str(self.id) + self.name + '.png'
        return path
