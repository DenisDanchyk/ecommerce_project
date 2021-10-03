from django.conf import settings
from django.shortcuts import render
from django.views.generic import DetailView, View
from django.core.paginator import Paginator


from . import models
from .forms import SearchForm
from .services import ProductSystem


def search_product(request):
    """ Search products by request """

    categories = ProductSystem.get_categories(self=ProductSystem)
    brands = ProductSystem.get_brands()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_request = form.cleaned_data['search_field']
            products = ProductSystem.search_products_by_request(
                self=ProductSystem,
                search_request=search_request)
    else:
        form = SearchForm()
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'store/products/products.html', {'products': page_obj,
                                                            'categories': categories,
                                                            'brands': brands,
                                                            'search_form': form,
                                                            })


class BaseView(View):
    """ Show main page """

    def get(self, request):
        products = ProductSystem.get_product_list_with_discount(
            self=ProductSystem,
            models=settings.PRODUCT_MODELS
        )
        return render(request, 'store/homepage.html', {'discount_products': products, })


class ProductListView(View):
    """ Show product list """

    def get(self, request, **kwargs):
        products = ProductSystem.get_product_list(
            models=settings.PRODUCT_MODELS
        )
        categories = ProductSystem.get_categories(self=ProductSystem)
        brands = ProductSystem.get_brands()
        search_form = SearchForm()

        if kwargs.get('category_slug'):
            category_slug = kwargs.get('category_slug')
            products = ProductSystem.get_product_list_by_category(self=ProductSystem,
                                                                  category_slug=category_slug,
                                                                  models=settings.PRODUCT_MODELS)

        if kwargs.get('brand_slug'):
            brand_slug = kwargs.get('brand_slug')
            products = ProductSystem.get_products_by_brand(self=ProductSystem, brand_slug=brand_slug,
                                                           models=settings.PRODUCT_MODELS)

        if kwargs.get('min_price'):
            min_price, max_price = kwargs.get(
                'min_price'), kwargs.get('max_price')
            products = ProductSystem.get_product_list_by_price(self=ProductSystem,
                                                               min_price=min_price,
                                                               max_price=max_price,
                                                               models=settings.PRODUCT_MODELS)
        paginator = Paginator(products, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'store/products/products.html', {'products': page_obj,
                                                                'categories': categories,
                                                                'brands': brands,
                                                                'search_form': search_form,
                                                                })


class ProductDetailView(DetailView):
    """ Show product detail page """

    CT_MODEL_MODEL_CLASS = {
        'clothesproduct': models.ClothesProduct,
        'shoesproduct': models.ShoesProduct,
        'bagproduct': models.BagProduct,
        'accessoriesproduct': models.AccessoriesProduct,
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        category_slug = context['product'].category.slug
        context['related_products'] = ProductSystem.get_product_list_by_category(self=ProductSystem,
                                                                                 category_slug=category_slug,
                                                                                 models=settings.PRODUCT_MODELS)
        context['related_products'].remove(context['product'])
        return context

    context_object_name = 'product'
    template_name = 'store/products/product_detail.html'
    slug_url_kwarg = 'product_slug'
