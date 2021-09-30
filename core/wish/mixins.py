from django.views.generic import View

from .services import get_or_create_wish, get_or_create_wish_for_anonymos


class WishMixin(View):
    """  Get or create with for customer """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            wish = get_or_create_wish(request)
        else:
            wish = get_or_create_wish_for_anonymos()
        self.wish = wish
        return super().dispatch(request, *args, **kwargs)
