from django.views.generic import View

from .services import WishSystem


class WishMixin(View):
    """  Get or create with for customer """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            wish = WishSystem.get_or_create_wish(
                self=WishSystem, request=request)
        else:
            wish = WishSystem.get_or_create_wish_for_anonymos(self=WishSystem)
        self.wish = wish
        return super().dispatch(request, *args, **kwargs)
