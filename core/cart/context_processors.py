from cart.models import Cart
from accounts.models import UserBase


def cart_products_count(request):
    """ Get cart products count """

    if request.user.is_authenticated:
        customer = UserBase.objects.get(email=request.user)
        cart = Cart.objects.filter(owner=customer, in_order=False).first()
        if not cart:
            cart = Cart.objects.create(owner=customer)
        cart_products_count = cart.products.count
        cart_final_price = cart.final_price
    else:
        cart_products_count = 0
        cart_final_price = 0
    return {'cart_products_count': cart_products_count,
            'cart_final_price': cart_final_price}
