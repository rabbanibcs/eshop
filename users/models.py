from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager
from products.models import Items


# Substituting a custom User model
class Users(AbstractUser):
    username = None
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100, unique=True)
    gender = models.CharField(max_length=1, default='F')
    # date_joined=models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', ]
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    # this appears alongside the username in an object’s history
    #  in django.contrib.admin.
    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)

    def __str__(self):
        return self.item.name


# Cart...
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"qty {self.quantity} of {self.item.name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        return self.get_total_discount_item_price()


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shipping_address = models.TextField(max_length=100, null=True)
    phone = models.CharField(max_length=11, null=True)
    zip = models.CharField(max_length=100)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.shipping_address

    class Meta:
        verbose_name_plural = 'Addresses'


# Check out...
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(Cart)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    address = models.ForeignKey(
        'Address', related_name='address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.OneToOneField(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.email+'---'+str(self.id)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


ORDER_STATUS = (
    ('P', 'Processing'),
    ('S', 'Shipping'),
    ('D', 'Delivered'),
    ('R', 'Refunded'),
)
PAYMENT_STATUS = (
    ('C', 'CashOnDelivery'),
    ('P', 'Paid'),
)


class ManageOrder(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    status = models.CharField(choices=ORDER_STATUS, max_length=1, default='P')
    payment = models.CharField(choices=PAYMENT_STATUS, max_length=1, default='P')

    def __str__(self):
        return self.order.user.email


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
