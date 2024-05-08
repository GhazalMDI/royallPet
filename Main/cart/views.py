from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.contrib import messages

from cart.cart import Cart, VariantCart
from products.models import Product, VariantProduct
from products.models import Like
from cart.forms import QuantityForm


# class CartView(LoginRequiredMixin, View):
#     template_name = 'cart/cart.html'
#
#     def get(self, request):
#         ctx = {
#             'cart': Cart(request)
#         }
#         return render(request, self.template_name, ctx)


class RemoveTofavouriteView(LoginRequiredMixin, View):
    def get(self, request):
        product = Product.objects.filter(id=request.GET.get('p_id')).first()
        if product:
            if obj := Like.objects.get(product=product, user=request.user):
                obj.delete()
                return HttpResponse('success')
            return HttpResponse('success')
        return HttpResponse('error')


class AddToCartView(LoginRequiredMixin, View):

    def post(self, request):
        print(request.POST.get('p_slug'))
        product = Product.objects.filter(slug__exact=request.POST.get('p_slug')).first()
        form = QuantityForm(request.POST)
        if product:
            if form.is_valid():
                quantity = form.cleaned_data['quantity']
            else:
                quantity = 1
            cart = Cart(request)
            res = cart.AddToCart(product, quantity)
            if res:
                return HttpResponse('success')
            else:
                messages.add_message(request, 200, 'لطفا مقدار درخواستی را کم کنید', 'danger')
        return HttpResponse('error')


class AddToCartFromLikeView(LoginRequiredMixin, View):
    def get(self, request, c_id):
        return redirect('Products:Products')

    def post(self, request, c_id):
        product = Product.objects.filter(id=c_id).first()
        if product:
            prod = Cart(request)
            res = prod.AddToCart(product, 1)
            if res:
                return redirect('Accounts:Profile')
            messages.add_message(request, 200, 'لطفا مقدار درخواستی را کم کنید', 'danger')
            return redirect('Home:home')
        return redirect('Home:home')


class AddOneToCartView(LoginRequiredMixin, View):
    def get(self, request):
        product_id = request.GET.get('p_id')
        print(product_id)
        if product_id:
            product = Product.objects.filter(id=product_id).first()
            if product:
                cart = Cart(request)
                cart.AddToCart(product, quantity=1)
                cart_data = cart.serialize_cart()
                return JsonResponse({'success': True, 'cart_data': cart_data})
            else:
                return JsonResponse({'success': False, 'error_message': 'محصول مورد نظر یافت نشد'})
        else:
            return JsonResponse({'success': False, 'error_message': 'لطفاً یک محصول انتخاب کنید'})


class DeleteOneToCartView(LoginRequiredMixin, View):
    def get(self, request):
        product_id = request.GET.get('c_id')
        if product_id:
            product = Product.objects.filter(id=product_id).first()
            if product:
                print('hi')
                cart = Cart(request)
                cart.remove(product, 1)
                print('yes')
                cart_data = cart.serialize_cart()
                print('HI')
                return JsonResponse({'success': True, 'cart_data': cart_data})
            else:
                return JsonResponse({'success': False, 'error_message': 'محصول مورد نظر یافت نشد'})
        else:
            return JsonResponse({'success': False, 'error_message': 'لطفاً یک محصول انتخاب کنید'})


class RemoveProduct(View):
    def get(self, request):
        product_id = request.GET.get('c_id')
        product = Product.objects.filter(id=product_id).first()
        if product:
            cart = Cart(request)
            cart.clear_object(product)
            print('HI')
            cart_data = cart.serialize_cart()
            print('hi')
            return JsonResponse(cart_data)
        return JsonResponse({'error': 'محصول مورد نظر یافت نشد'}, status=400)


#  Variant cart

class RemoveVarProduct(View):
    def get(self, request):
        product_id = request.GET.get('c_id')
        product = VariantProduct.objects.filter(id=product_id).first()
        if product:
            cart = VariantCart(request)
            cart.clear_object(product)
            print('HI')
            cart_data = cart.serialize_cart()
            print('hi')
            return JsonResponse(cart_data)
        return JsonResponse({'error': 'محصول مورد نظر یافت نشد'}, status=400)


class AddToVariantLikeCartView(LoginRequiredMixin, View):
    def get(self, request):
        product_id = request.GET.get('c_id')
        print(product_id)
        # if product_id:
        product = VariantProduct.objects.filter(id=product_id).first()
        if product:
            print('hi')
            cart = VariantCart(request)
            cart.AddToCart(product, quantity=1)
            cart_data = cart.serialize_cart()
            return JsonResponse({'success': True, 'cart_data': cart_data})
        else:
            return JsonResponse({'success': False, 'error_message': 'محصول مورد نظر یافت نشد'})


class AddToVariantCartView(LoginRequiredMixin, View):
    def get(self, request):
        product_id = request.GET.get('selected_size')
        print(product_id)
        # if product_id:
        product = VariantProduct.objects.filter(id=product_id).first()
        if product:
            print('hi')
            cart = VariantCart(request)
            cart.AddToCart(product, quantity=1)
            cart_data = cart.serialize_cart()
            return JsonResponse({'success': True, 'cart_data': cart_data})
        else:
            return JsonResponse({'success': False, 'error_message': 'محصول مورد نظر یافت نشد'})


# else:
# return JsonResponse({'success': False, 'error_message': 'لطفاً یک محصول انتخاب کنید'})

# class AddToVariantCartView(LoginRequiredMixin, View):
#     def get(self, request, product_id):
#         user_color = request.GET.get('selected_color')
#         user_size = request.GET.get('Selected_Size')
#         print("User Color:", user_color)
#         print("User Size:", user_size)
#
#         product = Product.objects.filter(id=product_id).first()
#         var_product = VariantProduct.objects.filter(color__id=user_color, size__id=user_size,
#                                                     product__id=product.id).first()
#
#         if var_product:
#             quantity = int(request.POST.get('quantity'))
#             cart = VariantCart(request)
#             res = cart.AddToCart(var_product, quantity)
#
#             if res:
#                 return redirect('Accounts:Profile')
#             messages.add_message(request, 200, 'لطفا مقدار درخواستی را کم کنید', 'danger')
#             return redirect('Home:home')

# return redirect('Products:Products')


class AddToVaraintCartFromLikeView(LoginRequiredMixin, View):

    def post(self, request, c_id):
        product = VariantProduct.objects.filter(id=c_id).first()
        if product:
            prod = VariantCart(request)
            res = prod.AddToCart(product, 1)
            if res:
                return redirect('Accounts:Profile')
            messages.add_message(request, 200, 'لطفا مقدار درخواستی را کم کنید', 'danger')
            return redirect('Home:home')
        return redirect('Home:home')


class RemoveToVarfavouriteView(LoginRequiredMixin, View):
    def get(self, request):
        product = VariantProduct.objects.filter(id=request.GET.get('p_id')).first()
        if product:
            if obj := Like.objects.get(var_product=product, user=request.user):
                obj.delete()
                return HttpResponse('success')
            return HttpResponse('error')
        return redirect('Products:Products')


class AddOneToVarCartView(LoginRequiredMixin, View):
    def get(self, request):
        product = VariantProduct.objects.filter(id=request.GET.get('v_id')).first()
        if product:
            prod = VariantCart(request)
            res = prod.AddToCart(product, 1)
            if res:
                return JsonResponse({'success': True, 'redirect_url': 'Accounts:Profile'})
            return JsonResponse({'success': False, 'error_message': 'لطفا مقدار درخواستی را کم کنید'})
        return JsonResponse({'success': False, 'error_message': 'محصول مورد نظر یافت نشد'})


class DeleteVariantProduct(LoginRequiredMixin, View):
    def get(self, request):
        product_id = request.GET.get('c_id')
        if product_id:
            product = Product.objects.filter(id=product_id).first()
            if product:
                print('hi')
                cart = Cart(request)
                cart.remove(product, 1)
                print('yes')
                cart_data = cart.serialize_cart()
                print('HI')
                return JsonResponse({'success': True, 'cart_data': cart_data})
            else:
                return JsonResponse({'success': False, 'error_message': 'محصول مورد نظر یافت نشد'})
        else:
            return JsonResponse({'success': False, 'error_message': 'لطفاً یک محصول انتخاب کنید'})
