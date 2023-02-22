from items.models import Item


class Order(object):
    def __init__(self, request):
        self.session = request.session
        order = self.session.get('order')
        if not order:
            order = self.session['order'] = {}
        self.order = order

    def __iter__(self):
        item_ids = self.order.keys()
        items = Item.objects.filter(id__in=item_ids)

        order = self.order.copy()
        for item in items:
            order[str(item.id)]['item'] = item

        for item in order.values():
            item['price'] = int(item['price'])
            item['total_price'] = int(item['price']) * int(item['quantity'])
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.order.values())

    def add(self, item, quantity=1, override_quantity=False):
        item_id = str(item.id)
        if item_id not in self.order:
            self.order[item_id] = {'quantity': 0, 'price': item.price}
        
        if override_quantity:
            self.order[item_id]['quantity'] = quantity
        else:
            self.order[item_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, item):
        item_id = str(item.id)
        if item_id in self.order:
            del self.order[item_id]
            self.save()

    def get_total_price(self):
        return sum(item['price'] * item['quantity'] for item in self.order.values())

    def clear(self):
        del self.session['order']
        self.save()