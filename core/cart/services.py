from django.db import models


from accounts.services import CustomerAccount
from store.services import _get_product, _get_content_type

from .models import CartProduct, Cart


def get_customer_cart(request):
    """ Get customer cart """

    cart = Cart.objects.get(owner=request.user, in_order=False)
    return cart


def get_customer_in_order_carts(customer):
    """ Get customer cart that have in_order=True """

    carts = Cart.objects.filter(owner=customer)
    return carts


def get_or_create_customer_cart(request):
    """ Get or create customer cart """

    if request.user.is_authenticated:
        cart = get_customer_cart(request)
        if not cart:
            cart = _create_customer_cart(request)
    else:
        cart = get_cart_for_anonymos()
        if not cart:
            cart = _create_cart_for_anonymos()
    return cart


def get_cart_for_anonymos():
    """ Get cart for anonymos user """

    cart = Cart.objects.filter(for_anonymos_user=True).first()
    return cart


def get_cart_products(cart):
    """ Get cart products """

    cart_products = CartProduct.objects.all().filter(cart=cart)
    return cart_products


def get_or_create_cart_product(kwargs, cart):
    """ Get or create product for cart """

    product = _get_product(kwargs)
    content_type = _get_content_type(kwargs)
    cart_product, create = CartProduct.objects.get_or_create(
        user=cart.owner, cart=cart, content_type=content_type, object_id=product.id,
    )
    return cart_product, create


def get_cart_product(kwargs, cart):
    """ Get product for cart """

    product = _get_product(kwargs)
    content_type = _get_content_type(kwargs)
    cart_product = CartProduct.objects.get(
        user=cart.owner, cart=cart, content_type=content_type, object_id=product.id,
    )
    return cart_product


def add_product_to_cart(request, cart, cart_product, create):
    """ Add product to cart """

    if create:
        if request.POST.get('add_product_quantity'):
            _add_product_quantity(request, cart_product=cart_product)
        cart.products.add(cart_product)
    else:
        if request.POST.get('add_product_quantity'):
            _add_product_quantity(request, cart_product=cart_product)
        else:
            cart_product.quantity += 1
    _add_product_size(request, cart_product=cart_product)
    _save_cart_product(cart_product=cart_product)


def remove_product_from_cart(cart, cart_product):
    """ Remove cart product """

    cart.products.remove(cart_product)
    cart_product.delete()
    _save_cart(cart=cart)


def change_product_quantity(request, cart_product, cart):
    """ Change cart product quantity """

    product_quantity = int(request.POST.get('product_quantity'))
    cart_product.quantity = product_quantity
    _save_cart_product(cart_product=cart_product)
    _save_cart(cart=cart)
    return product_quantity


def recal_total_products_in_cart(cart):
    """ Recalculation total products count and cart final price """

    cart_data = cart.products.aggregate(
        models.Sum('final_price'), models.Count('id'))
    if cart_data.get('final_price__sum'):
        cart.final_price = cart_data['final_price__sum']
    else:
        cart.final_price = 0
    cart.total_products = cart_data['id__count']
    _save_cart(cart=cart)


def _save_cart_product(cart_product):
    """ Save product for cart """

    cart_product.save()


def _save_cart(cart):
    """ Save cart """

    cart.save()


def _add_product_quantity(request, cart_product):
    """ Add product quantity to cart product"""

    add_product_quantity = int(request.POST.get('add_product_quantity'))
    cart_product.quantity += add_product_quantity


def _add_product_size(request, cart_product):
    """ Set product size """

    if request.POST.get('add_product_size'):
        product_size = request.POST.get('add_product_size')
        cart_product.user_size_choice = product_size


def _create_cart_for_anonymos():
    """ Create cart for anonymos customer """

    cart = Cart.objects.create(for_anonymos_user=True)
    return cart


def _create_customer_cart(request):
    """ Create cart for customer """

    customer = get_customer_account(request)
    cart = Cart.objects.create(owner=customer)
    return cart
