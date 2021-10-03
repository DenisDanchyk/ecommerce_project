from cart.services import CustomerCart

from .models import Order, OrderItem


class OrderSystem:
    """ Manipulate with customer orders """

    def get_user_orders(customer, cart):
        """ Get customer orders in_order=True"""

        orders = []
        for order in Order.objects.all():
            if order.customer == customer and cart == cart:
                orders.append(order)
        return orders

    def get_order_items():
        """ Get order items """

        order_items = OrderItem.objects.all()
        return order_items

    def create_order(self, form, cart):
        """ Create order """

        cart_products = CustomerCart.get_cart_products(cart=cart)
        customer = cart.owner

        if form.is_valid() and cart_products:
            order = self._create_order_data(
                form=form, cart=cart, customer=customer)
            self._create_order_item(cart_products=cart_products, order=order)

            cart.in_order = True
            cart.save()
            return order
        return False

    def _create_order_data(form, cart, customer):
        """ Create order data """

        new_order = form.save(commit=False)
        new_order.customer = customer
        new_order.cart = cart
        new_order.first_name = form.cleaned_data['first_name']
        new_order.last_name = form.cleaned_data['last_name']
        new_order.phone = form.cleaned_data['phone']
        new_order.city = form.cleaned_data['city']
        new_order.post_office = form.cleaned_data['post_office']
        new_order.email = form.cleaned_data['email']
        new_order.comment = form.cleaned_data['comment']
        new_order.save()
        customer.orders.add(new_order)
        return new_order

    def _create_order_item(order, cart_products):
        """ Create order item """

        for cart_product in cart_products:
            OrderItem.objects.create(
                order=order, content_type=cart_product.content_type,
                object_id=cart_product.object_id, price=cart_product.content_object.price, quantity=cart_product.quantity)
