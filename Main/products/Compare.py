COMPARE_ID = 'Compare'
from products.models import Product


class Compare:
    def __init__(self, request):
        self.session = request.session
        if not self.session.get(COMPARE_ID):
            self.session[COMPARE_ID] = {}
        self.compare = self.session.get(COMPARE_ID)

    def save(self):
        self.session.modified = True

    def __len__(self):
        return len(self.session[COMPARE_ID])

    def AddToCompare(self, product):

        product_id = str(product.id)
        # if product_id not in self.compare:
        self.compare[product_id] = {'id': product.id, 'slug': product.slug, 'price': product.price,
                                    'category_two': product.category2.id,
                                    'category': product.category.name}
        self.save()
        # else:
        #     del self.compare[product_id]
        #     self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.compare:
            del self.compare[product_id]
            self.save()
        # if len(self.compare) == 0:
        #     del self.session[COMPARE_ID]

    def clearCompare(self, request):
        request.session.get(COMPARE_ID).clear()

    def __iter__(self):
        product_ids = self.compare.keys()
        products = Product.objects.filter(id__in=product_ids)
        compare = self.compare.copy()
        for p in products:
            compare[str(p.id)]['name'] = p.name
            compare[str(p.id)]['discount'] = p.discount
            compare[str(p.id)]['after_discount'] = p.after_discount
            compare[str(p.id)]['image'] = p.image.url
            compare[str(p.id)]['desc'] = p.desc
            compare[str(p.id)]['brand'] = p.brand.name
            compare[str(p.id)]['weight'] = p.weight

        for item in compare.values():
            yield item

    # def last(self, request):
    #     items = request.session.get(COMPARE_ID)
    #     # for last_item in items:
    #     if items:
    #         return list(items).index(0)
    #         # return list(last_item).index(0)
