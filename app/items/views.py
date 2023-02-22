from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views import View

from .models import Item
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class ItemsView(ListView):
    model = Item
    context_object_name = 'items'
    template_name = 'items/item_list.html'


class ItemView(DetailView):
    model = Item
    # context_object_name = 'item'
    template_name = 'items/item_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item'] = self.object
        context['STRIPE_PUBLIC_KEY'] = settings.STRIPE_PUBLIC_KEY
        return context


class CreateCheckoutSessionView(View):
    def post(self, request, pk):
        item = Item.objects.get(pk=pk)
        domain = 'http://' + request.get_host()
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': item.price * 100,
                        'product_data': {
                            'name': item.name,
                            'description': item.description
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": item.id
            },
            mode='payment',
            success_url= domain + '/success/',
            cancel_url= domain + '/cancel/',
        )

        return redirect(checkout_session.url, code=303)
