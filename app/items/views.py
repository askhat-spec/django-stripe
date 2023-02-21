from django.views.generic import ListView, DetailView

from .models import Item


class ItemsView(ListView):
    model = Item
    context_object_name = 'items'
    template_name = 'items/item_list.html'


class ItemView(DetailView):
    model = Item
    context_object_name = 'item'
    template_name = 'items/item_detail.html'
