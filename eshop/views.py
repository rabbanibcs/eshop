from django.shortcuts import render, get_object_or_404, redirect

from users.models import Cart,Address,Order


def index(request):
    # cart_item = Cart.objects.all()
    # for i in cart_item:
    #     print(i.order_set.all(),'<-cart')
    #     # i.delete()

    # ads=Address.objects.all()
    # for i in ads:
    #     print(i,'<-address')
    #     # i.delete()
    # ord=Order.objects.all()
    # for i in ord:
    #     print(i.items.all(),'<-order')
    #     # i.delete()
    return redirect('products')

def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')
