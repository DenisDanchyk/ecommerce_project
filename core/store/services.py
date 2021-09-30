from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.contrib.postgres.search import SearchVector, SearchQuery

from .models import (Category, Brand, ClothesProduct, ShoesProduct,
                     BagProduct, AccessoriesProduct, get_models_for_count)


def get_product_list(models):
    """ Get list of products """

    products = []
    ct_models = ContentType.objects.filter(model__in=models)
    for ct_model in ct_models:
        model_product = ct_model.model_class()._base_manager.all().order_by('-id')
        products.extend(model_product)
    return products


def get_product_list_with_discount(models):
    """ Get list of products that have discount """

    products = get_product_list(models=models)
    for item in products:
        if not item.discount_price:
            products.remove(item)

    return products


def get_product_list_by_price(min_price, max_price, models):
    """ Sort list by price """

    product_list = get_product_list(models=models)
    products = []
    for item in product_list:
        if item.discount_price:
            if item.discount_price > int(min_price) and item.discount_price < int(max_price):
                products.append(item)
        else:
            if item.price > int(min_price) and item.price < int(max_price):
                products.append(item)
    return products


CATEGORY_NAME_COUNT_NAME = {
    'Одяг': 'clothes_product__count',
    'Взуття': 'shoes_product__count',
    'Рюкзаки': 'bag_product__count',
    'Аксесуари': 'accessories_product__count'
}


def get_categories():
    """ Get dict of categories with new value count """

    models = get_models_for_count(
        'clothes_product', 'shoes_product', 'bag_product', 'accessories_product')
    qs = Category.objects.all().annotate(*models).values()
    return [dict(name=c['name'], slug=c['slug'],
                 get_absolute_url=reverse("store:product_list_by_category", kwargs={
                                          "category_slug": c['slug']}),
                 count=c[CATEGORY_NAME_COUNT_NAME[c['name']]]) for c in qs]


def get_product_list_by_category(category_slug, models):
    """ Sort list of products by category """

    product_list = get_product_list(models=models)
    products = []
    for product in product_list:
        if product.category.slug == category_slug:
            products.append(product)
    return products


def get_products_by_brand(brand_slug, models):
    """ Sort list of products by brand """

    product_list = get_product_list(models=models)
    products = []
    for item in product_list:
        if item.brand.slug == brand_slug:
            products.append(item)
    return products


def get_brands():
    """ Get brands """

    brands = Brand.objects.all().order_by('-id')
    return brands


def get_products_queryset_by_model(model, search_request):
    """ Get products queryset by model """

    products = model.annotate(search=SearchVector(
        'name', 'description',),).filter(search=SearchQuery(search_request))
    return products


def search_products_by_request(search_request):
    """ Search products by request """

    products = get_products_queryset_by_model(
        model=ClothesProduct.objects.all(), search_request=search_request)
    if not products:
        products = get_products_queryset_by_model(
            model=ShoesProduct.objects.all(), search_request=search_request)
    if not products:
        products = get_products_queryset_by_model(
            model=AccessoriesProduct.objects.all(), search_request=search_request)
    if not products:
        products = get_products_queryset_by_model(
            model=BagProduct.objects.all(), search_request=search_request)
    return products


def _get_content_type(kwargs):
    """ Get model by content type """

    ct_model = kwargs.get('ct_model')
    content_type = ContentType.objects.get(model=ct_model)
    return content_type


def _get_product(kwargs):
    """ Get product """

    product_slug = kwargs.get('product_slug')
    content_type = _get_content_type(kwargs)
    product = content_type.model_class().objects.get(slug=product_slug)
    return product
