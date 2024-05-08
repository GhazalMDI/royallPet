from products.models import Product, VariantProduct

CART_PRODUCT_ID = 'cart'
CART_VARIANT_ID = 'cartVariant'


class Cart:
    def __init__(self, request):
        self.session = request.session
        if not self.session.get(CART_PRODUCT_ID):
            self.session[CART_PRODUCT_ID] = {}
        self.cart = self.session.get(CART_PRODUCT_ID)

    def save(self):
        self.session.modified = True

    def AddToCart(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price),
                                     'after_discount': str(product.after_discount),
                                     'profit': str(product.profit_product)
                                     }
        if self.cart[product_id]['quantity'] + quantity > product.stock:
            return False

        self.cart[product_id]['quantity'] += quantity
        self.save()
        return True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for p in products:
            cart[str(p.id)]['name'] = p.name
            cart[str(p.id)]['discount'] = p.discount
            cart[str(p.id)]['image'] = p.image.url
            cart[str(p.id)]['id'] = p.id
            cart[str(p.id)]['after_discount'] = p.after_discount
            cart[str(p.id)]['profit'] = p.profit_product

        for item in cart.values():
            item['total'] = item['quantity'] * item['after_discount']
            item['total_fit'] = item['quantity'] * item['profit']
            yield item

    @property
    def get_total_price(self):
        return sum(
            i['quantity'] * int(i['after_discount']) for i in self.cart.values()
        )

    @property
    def get_total_profit(self):
        return sum(
            int(i['quantity']) * int(i['profit']) for i in self.cart.values() if i['profit'] and i['profit'] != 'False'
        )

    def __len__(self):
        return sum(
            1 for i in self.cart.values()
        )

    def remove(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            if self.cart[product_id]['quantity'] > 1:
                self.cart[product_id]['quantity'] -= quantity
            else:
                print('hi del ')
                del self.cart[product_id]
        self.save()

    def clear_object(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def serialize_cart(self):
        total_price = sum(int(item['quantity']) * int(item['price']) for item in self.cart.values())
        profit = sum(
            int(i['quantity']) * int(i['profit']) for i in self.cart.values() if i['profit'] and i['profit'] != 'False')
        cart_items = [
            {
                'id': item_id,
                'name': item_data['name'],
                'price': item_data['price'],
                'quantity': item_data['quantity'],
                'profit': item_data['profit'],
                'total': item_data['quantity'] * item_data['price'],
            }
            for item_id, item_data in self.cart.items()
        ]

        return {
            'cart_length': len(self),
            'products': cart_items,
            'total_price': total_price,
            'profit': profit,
        }


class VariantCart:
    def __init__(self, request):
        self.session = request.session
        if not self.session.get('CART_VARIANT_ID'):
            self.session['CART_VARIANT_ID'] = {}
        self.variant_cart = self.session.get('CART_VARIANT_ID')

    def save(self):
        self.session.modified = True

    def AddToCart(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.variant_cart:
            self.variant_cart[product_id] = {'quantity': 0, 'price': str(product.price),
                                             'after_discount': str(product.after_discount),
                                             'profit': str(product.profit_product),
                                             'discount': product.discount,
                                             'image': product.product.image.url,
                                             'name': product.product.name,
                                             'size': product.size.name,
                                             'id': product.id
                                             }
        if self.variant_cart[product_id]['quantity'] + quantity > product.stock:
            return False

        self.variant_cart[product_id]['quantity'] += quantity
        self.save()
        return True

    def __iter__(self):
        for item in self.variant_cart.values():
            item['total'] = item['quantity'] * int(item['after_discount'])
            item['total_fit'] = item['quantity'] * int(item['profit'])
            yield item

    @property
    def get_total_price(self):
        return sum(
            i['quantity'] * int(i['after_discount']) for i in self.variant_cart.values()
        )

    @property
    def get_total_profit(self):
        return sum(
            int(i['quantity']) * int(i['profit']) for i in self.variant_cart.values() if
            i['profit'] and i['profit'] != 'False'
        )

    def __len__(self):
        return sum(
            1 for i in self.variant_cart.values()
        )

    def remove(self, product, quantity=None):
        product_id = str(product.id)
        if product_id in self.variant_cart:
            if not quantity:
                del self.variant_cart[product_id]
                self.save()
            else:
                if self.variant_cart[product_id]['quantity'] > 1:
                    self.variant_cart[product_id]['quantity'] -= quantity
                    self.save()
                else:
                    self.remove(product)

    def clear_object(self, product):
        product_id = str(product.id)
        if product_id in self.variant_cart:
            del self.variant_cart[product_id]
            self.save()

    def serialize_cart(self):
        total_price = sum(int(item['quantity']) * int(item['price']) for item in self.variant_cart.values())
        profit = sum(
            int(i['quantity']) * int(i['profit']) for i in self.variant_cart.values() if i['profit'] and i['profit'] != 'False')
        cart_items = [
            {
                'id': item_id,
                'name': item_data['name'],
                'price': item_data['price'],
                'quantity': item_data['quantity'],
                'profit': item_data['profit'],
                'total': item_data['quantity'] * item_data['price'],
            }
            for item_id, item_data in self.variant_cart.items()
        ]

        return {
            'cart_length': len(self),
            'products': cart_items,
            'total_price': total_price,
            'profit': profit,
        }
