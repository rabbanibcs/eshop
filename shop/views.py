from django.shortcuts import render
from django.views import View

from shop.models import Product,Category


class ProductView(View):

    def get(self, request):
        category = Category.objects.all()
        print(request.GET.get('category'))
        if request.GET.get('category') :
            products = Product.objects.filter(category_id=request.GET.get('category'))

        else:
            products = Product.objects.all()
        context = {'products': products, 'category': category}
        return render(request, 'shop/shop.html', context)



        # category = Category.objects.all()
        # if request.GET.get('category'):
        #     products = Product.objects.filter(category=request.GET.get('category'))
        # else:
        #     products = Product.objects.all()
        # if request.user.is_authenticated:
        #     customer = request.user.customer
        #     order, created = Order.objects.get_or_create(customer=customer, complete=False)
        #     context = {'products': products, 'order': order, 'category': category}  # problem solved
        # else:
        #
        #     context = {'products': products, 'category': category}
        # return render(request, 'store/store.html', context)
