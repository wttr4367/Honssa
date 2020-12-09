from django.shortcuts import render, redirect
from admin.models import *

def honssa_main(request):
    product_list = product_tbl.objects.all()
    products = []
    for i in range(8):
        products.append(product_list[i])
    return render(request, 'honssauser/main.html', {'product': products})

def honssa_cart(request):
    id = request.user.id
    member = member_tbl.objects.get(id= id)
    if cart_tbl.objects.filter(member_number = member.id):
        cart = cart_tbl.objects.filter(member_number = member.id)
    else:
        cart = None
    context = {'cart': cart, 'member': member}
    return render(request, 'honssauser/cart.html', context)

def cart_delete(request, id):
    cart = cart_tbl.objects.get(id=id)
    cart.delete()
    return redirect('../')

def honssa_payment(request):
    print(request.POST)
    cart = request.POST.getlist('cart_id')
    return render(request, 'honssauser/payment.html', {'cart': cart})

def honssa_order(request):
    return render(request, 'honssauser/order.html', {})

def honssa_create(request):
    # cart = Cart(request)
    # if request.method == 'POST':
    #     form = OrderCreateForm(request.POST)
    #     if form.is_valid():
    #         order = form.save()
    #         for item in cart:
    #             OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
    #                                      quantity=item['quantity'])
    #
    #         cart.clear()
    #         return render(request, 'order/create.html', {'order':order})
    #
    # else:
    #     form = OrderCreateForm()
    cart_list = request.POST.getlist('cart')

    price = 0
    for cart_id in cart_list:
        cart = cart_tbl.objects.get(id = cart_id)
        price += cart.cart_product_price
    print(price)
    content = {'price': price}
    return render(request, 'honssauser/create.html', content)
    # 위 괄호에 들어갈것'cart':cart, 'form':form

def product_detail(request, id):
    product = product_tbl.objects.get(id = id)
    return render(request, 'honssauser/product-detail.html', {'product':product})

def cart_insert(requset):
    user = member_tbl.objects.get(member_id=requset.user)
    product = product_tbl.objects.get(id=requset.POST['product'])
    quantity = requset.POST['quantity']
    price = product.product_Price * int(quantity)
    print(user, product, quantity, price)
    cart = cart_tbl(cart_product_price= price,
                 cart_quantity= quantity,
                 member_number= user,
                 product_number= product)
    cart.save()
    return redirect('honssauser:cart')


# Create your views here.
