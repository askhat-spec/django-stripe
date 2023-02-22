from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from items.models import Item
from .order import Order
from .forms import OrderAddItemForm


@require_POST
def order_add(request, item_id):
    order = Order(request)
    item = get_object_or_404(Item, id=item_id)
    form = OrderAddItemForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        order.add(
            item=item,
            quantity=cd['quantity'],
            override_quantity=cd['override'],
        )
    return redirect(request.META['HTTP_REFERER'])


@require_POST
def order_remove(request, item_id):
    order = Order(request)
    item = get_object_or_404(Item, id=item_id)
    order.remove(item)
    return redirect('order_detail')


def order_detail(request):
    order = Order(request)
    for item in order:
        item['update_quantity_form'] = OrderAddItemForm(initial={
            'quantity': item['quantity'],
            'override': True
        })
    return render(request, 'order/detail.html', {'order': order})
