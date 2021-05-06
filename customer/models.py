from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField(max_length=11)
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name
