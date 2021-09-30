from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField, ModelForm
from django.utils.safestring import mark_safe


from PIL import Image

from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}


@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}


# class InlineImage(admin.TabularInline):
#     model = models.AdditionalImages

class ProductsAdminForm(ModelForm):
    """
        Allert in the admin panel about the required image requirement.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[
            'image'].help_text = mark_safe(f"""<span style=color:red; font-size:14px;>Загружайте зображення з мінімальним розширенням {models.Product.MIN_RESOLUTION}
                                                та максимальним {models.Product.MAX_RESOLUTION}</span>""")

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)   # Open image using lib
        min_height, min_width = models.Product.MIN_RESOLUTION
        max_height, max_width = models.Product.MAX_RESOLUTION
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Розмір зображення менше мінімального! ')
        if img.height > max_height or img.width > max_width:
            raise ValidationError(
                'Розмір зображення більший максимально дозволеного! ')
        return image


class ShoesProductAdmin(admin.ModelAdmin):
    form = ProductsAdminForm

    list_display = ['name', 'slug', 'price', 'in_stock', 'created', 'updated']
    list_filter = ['in_stock', 'is_active', 'price']
    list_editable = ['price', 'in_stock']
    prepopulated_fields = {'slug': ('name',)}

    """
        Permission to select only approprivate category to the class 
    """

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(models.Category.objects.filter(slug='vzuttya'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ClothesProductAdmin(admin.ModelAdmin):
    form = ProductsAdminForm

    list_display = ['name', 'slug', 'price', 'in_stock', 'created', 'updated']
    list_filter = ['in_stock', 'is_active', 'price']
    list_editable = ['price', 'in_stock']
    prepopulated_fields = {'slug': ('name',)}

    """
        Permission to select only approprivate category to the class 
    """

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(models.Category.objects.filter(slug='odyag'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class BagProductAdmin(admin.ModelAdmin):
    form = ProductsAdminForm

    list_display = ['name', 'slug', 'price', 'in_stock', 'created', 'updated']
    list_filter = ['in_stock', 'is_active', 'price']
    list_editable = ['price', 'in_stock']
    prepopulated_fields = {'slug': ('name',)}

    """
        Permission to select only approprivate category to the class 
    """

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(models.Category.objects.filter(slug='ryukzaki'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class AccessoriesProductAdmin(admin.ModelAdmin):
    form = ProductsAdminForm

    """
        
    """
    list_display = ['name', 'slug', 'price', 'in_stock', 'created', 'updated']
    list_filter = ['in_stock', 'is_active', 'price']
    list_editable = ['price', 'in_stock']
    prepopulated_fields = {'slug': ('name',)}

    """
        Permission to select only approprivate category to the class 
    """

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(models.Category.objects.filter(slug='aksesuari'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(models.ShoesProduct, ShoesProductAdmin)
admin.site.register(models.ClothesProduct, ClothesProductAdmin)
admin.site.register(models.BagProduct, BagProductAdmin)
admin.site.register(models.AccessoriesProduct, AccessoriesProductAdmin)
