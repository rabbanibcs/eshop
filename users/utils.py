
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils import timezone
from products.utils import add_to_cart_for_authenticated_user
from products.models import Items
from users.models import Cart


def create_cart_while_logged_in(request, cart):
    for item_id, qty in cart.items():
        add_to_cart_for_authenticated_user(request, int(item_id), qty)


def confirm_order(order, payment=None):
    order_items = order.items.all()
    order_items.update(ordered=True)
    for item in order_items:
        item.save()
    order.ordered = True
    order.ordered_date = timezone.now()
    # if payment:
    #     order.payment = payment
    # order.address=address
    order.save()
