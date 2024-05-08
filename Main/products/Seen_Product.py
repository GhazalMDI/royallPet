from products.models import Product

SEEN_PRODUCT = 'SEEN'


class SeenProduct:

    def __init__(self, request):
        self.session = request.session
        if not self.session.get(SEEN_PRODUCT):
            self.session[SEEN_PRODUCT] = {}
        self.seen = self.session.get(SEEN_PRODUCT)

    def save(self):
        self.session.modified = True

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.seen:
            if len(self.session['SEEN']) <= 10:
                self.seen[product_id] = {'slug': product.slug, 'id': product.id}
            else:
                self.seen.popitem()
                print(self.seen)
                # last_product_id = self.seen.get('product_seen', [])[-1]
                # last_product = self.seen.get(last_product_id)
                # print(last_product)
                # last_product_session = self.seen[product_id].pop(0)
                # del self.seen[last_product_session]
                self.seen[product_id] = {'slug': product.slug, 'id': product.id}

    def __iter__(self):
        product_ids = self.seen.keys()
        product = Product.objects.filter(id__in=product_ids)
        seen = self.seen.copy()
        for p in product:
            seen[str(p.id)]['id'] = p.id
            seen[str(p.id)]['name'] = p.name
            seen[str(p.id)]['image'] = p.image.url
            seen[str(p.id)]['price'] = p.price
            seen[str(p.id)]['after_discount'] = p.after_discount
        for item in seen.values():
            yield item

    def __len__(self):
        return len(self.session['SEEN'])
