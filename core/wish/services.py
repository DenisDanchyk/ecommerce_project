from accounts.services import AccountSystem

from store.services import ProductSystem

from .models import Wish, WishProduct


def get_or_create_wish(request):
    """ Get or create wish for customer """

    customer = AccountSystem.get_customer_account(request)
    wish = _get_customer_wish(customer=customer)
    if not wish:
        wish = _create_customer_wish(customer=customer)
    return wish


def get_or_create_wish_for_anonymos():
    """  Get or create wish for anonymos customer """

    wish = _get_wish_for_anonymos()
    if not wish:
        wish = _create_wish_for_anonymos()
    return wish


def get_or_create_wish_product(self, wish, **kwargs):
    """ Get or create wish product """

    content_type = ProductSystem._get_content_type(kwargs=kwargs)
    product = ProductSystem._get_product(self, kwargs=kwargs)

    wish_product, create = WishProduct.objects.get_or_create(
        user=wish.owner, wish=wish, content_type=content_type, object_id=product.id
    )

    return wish_product, create


def get_wish_product(self, wish, **kwargs):
    """ Get wish product """

    content_type = ProductSystem._get_content_type(kwargs=kwargs)
    product = ProductSystem._get_product(self, kwargs=kwargs)
    wish_product = WishProduct.objects.get(
        user=wish.owner, wish=wish, content_type=content_type, object_id=product.id
    )
    return wish_product


def add_product_to_wish(wish, wish_product):
    """ Add product to wish """

    wish.products.add(wish_product)


def save_wish(wish):
    """ Save wish """

    wish.save()
    return wish


def remove_wish_product(wish, wish_product):
    """ Remove product from wish """

    wish.products.remove(wish_product)
    wish_product.delete()


def _get_customer_wish(customer):
    """ Get customer wish """

    wish = Wish.objects.filter(owner=customer).first()
    return wish


def _create_customer_wish(customer):
    """ Create wish for customer """

    wish = Wish.objects.create(owner=customer)
    return wish


def _get_wish_for_anonymos():
    """ Get wish for anonymos customer """

    wish = Wish.objects.filter(for_anonymos_user=True).first()
    return wish


def _create_wish_for_anonymos():
    """ Create wish for anonymos customer """

    wish = Wish.objects.create(for_anonymos_user=True)
    return wish
