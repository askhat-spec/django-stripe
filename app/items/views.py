from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views import View

from order.forms import OrderAddItemForm
from order.order import Order

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
        context['order_form'] = OrderAddItemForm()
        return context


class CreateCheckoutSessionView(View):
    def post(self, request):
        order = Order(request)
        domain = 'http://' + request.get_host()
        # items = [{'product_id': item[0], **item[1]} for item in order.order.items()]
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': order.get_total_price() * 100,
                        'product_data': {
                            'name': 'test'
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url= domain + '/success/',
            cancel_url= domain + '/cancel/',
        )

        return redirect(checkout_session.url, code=303)
