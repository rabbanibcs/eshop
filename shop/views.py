from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from shop.models import Product, Category, Customer, Cart, Order



class ProductsView(View):

    def get(self, request):
        category = Category.objects.all()
        if request.GET.get('query'):
            products = Product.objects.filter(name=request.GET.get('query'))
            if products:
                pass
            else:
                messages.warning(request,'No product found.')

        else:
            products = Product.objects.all()


        context = {'products': products, 'category': category}
        return render(request, 'shop/shop.html', context)

    def post(self, request):

        if request.POST.get('category'):
            category_id = request.POST.get('category')
            products = Product.objects.filter(category_id=category_id)
            product_id = Product.objects.filter(category_id=category_id)
            context = {'product_id': product_id, 'products': products}
            print('category_id', category_id)
            return render(request, 'shop/shop.html', context)
        if request.POST.get('product_id'):
            product_id = request.POST.get('product_id')
            print('product_id', product_id)
            product = Product.objects.filter(id=product_id)
            stock = Product.objects.get(pk=product_id).stock
            print(stock)
            context = {'stock': stock, 'products': product, 'id': product_id}
            return render(request, 'shop/shop.html', context)

        if request.POST.get('quantity'):
            product_id = request.POST.get('product')
            quantity = request.POST.get('quantity')
            stock = Product.objects.get(pk=product_id).stock

            if int(quantity) > stock:
                messages.error(request, 'Sorry, Quantity is more than Stock')
            else:
                self.add_to_cart(request, product_id, quantity)

            category = Category.objects.all()
            products = Product.objects.all()
            context = {'category': category, 'products': products}

            print('quantity', quantity)
            print('product_id', product_id)
            return render(request, 'shop/shop.html', context)

        if request.POST.get('id'):
            product_id = request.POST.get('id')

            print(product_id)
            self.add_to_cart(request, product_id)

            return redirect('shop')

    @staticmethod
    def add_to_cart(request, product_id, quantity=1):
        pk = product_id
        q = int(quantity)
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(pk)
            # print(quantity)
            if quantity:
                cart[pk] = (q + quantity)
            else:
                cart[pk] = q
        else:
            cart = {pk: 1}
        print(cart)
        # items = ProductsView.total_cart_items(cart)
        # print(items)
        request.session['cart'] = cart
        # request.session['items'] = items
        messages.success(request, 'Added to the Cart. ')


class CartView(View):

    def get(self, request):

        cart = request.session.get('cart')
        print(cart)
        products = {}
        if cart:
            for product_id, quantity in cart.items():
                product = Product.objects.get(pk=product_id)
                products[product] = quantity

        context = {'products': products, }
        return render(request, 'shop/cart.html', context)

    def post(self, request):
        if request.POST.get('product'):
            pro_id = request.POST.get('product')
            del request.session['cart'][pro_id]
        request.session.save()
        cart = request.session.get('cart')
        print(cart)
        products = {}

        for product_id, quantity in cart.items():
            product = Product.objects.get(pk=product_id)
            products[product] = quantity

        context = {'products': products, }
        return render(request, 'shop/cart.html', context)


class OrderView(View):
    def post(self, request):
        if request.POST.get('email'):
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')

            customer = Customer(name=name, phone=phone, email=email)
            customer.save()
            qrcode_path=customer.qrcode_create()
            customer.qrcode=qrcode_path
            customer.save()
            order = Order(customer=customer, )
            order.save()
            cart = request.session.get('cart')
            if cart:
                for product_id, quantity in cart.items():
                    cart = Cart(product_id=product_id, quantity=quantity, order=order, complete=True)
                    cart.save()
                del request.session['cart']
                request.session.save()
        cart=order.cart_set.all()
        context={'cart':cart,'order':order}
        return render(request, 'shop/order.html',context)

    def get(self, request):
        order=Order.objects.get(pk=15)
        cart=order.cart_set.all()
        # word=num2words(987)

        # cart['word']=word
        print(cart)

        context={'cart':cart,'order':order}
        return render(request, 'shop/order.html',context)

    # def post(self, request):
    #     if request.user.is_authenticated:
    #         less = request.POST.get('less')
    #         if less:
    #             item = CartItem.objects.get(pk=less)
    #             if item.quantity >= 1:
    #                 item.quantity -= 1
    #                 item.save()
    #                 if item.quantity == 0:
    #                     item.delete()
    #         else:
    #             item = CartItem.objects.get(pk=request.POST['more'])
    #             item.quantity += 1
    #             item.save()
    #         return redirect('cart')

#
# class Index(View):
#     def get(self, request):
#         category = Category.objects.all()
#         context = {'categorys': category}
#
#         return render(request, 'shop/shop2.html', context)
#
#     def post(self, request):
#
#         if request.POST.get('category'):
#             category_id = request.POST.get('category')
#             products = Product.objects.filter(category_id=category_id)
#             context = {'products': products}
#             print(category_id)
#
#         if request.POST.get('product'):
#             product_id = request.POST.get('product')
#             product = Product.objects.get(pk=product_id)
#             stock = product.stock
#             context = {'stock': stock}
#             print(product_id)
#
#         if request.POST.get('quantity'):
#             quantity = request.POST.get('quantity')
#             category = Category.objects.all()
#             context = {'categorys': category}
#
#             print(quantity)
#
#         return render(request, 'shop/shop2.html', context)
