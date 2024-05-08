from cart.cart import Cart,VariantCart

def context_cart(request):
    return {
        'cart_len':Cart(request).__len__() + VariantCart(request).__len__()
    }