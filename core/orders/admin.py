from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'phone', 'email', 'city', 'post_office', 'comment', 'status']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
