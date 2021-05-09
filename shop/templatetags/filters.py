from django import template
from num2words import num2words
register = template.Library()


@register.filter(name='total_price')
def total_price(product, quantity):
    price = product.price * quantity
    return price


@register.filter(name='total_cart_items')
def total_cart_items(cart):
    total = 0
    if cart:
        for _, quantity in cart.items():
            total += quantity
    return total


@register.filter(name='num2word')
def num2word(price):
    return num2words(price)

@register.filter(name='price')
def total_price_in_order(cart):
    price=0
    for product in cart:
        price += product.product.price*product.quantity
    return price

