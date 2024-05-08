from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from urllib.parse import urlencode
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from products.models import Like
from products.models import Product, Category, CategorySecond, CategorySub, NewProduct, VariantProduct, Comment
from products.filter import ProductFilter
from utils.get_ip import get_client_ip
from cart.forms import QuantityForm
from products.Seen_Product import SeenProduct
from products.Compare import Compare
from products.forms import CommentForm


class ProductsView(View):
    template_name = 'products/Product.html'

    def get(self, request, id=None, slug=None, brand_id=None):
        products = Product.objects.filter(is_available=True)

        if 'all' in request.GET:
            print('hi')
            products = products.order_by('-created')

        if brand_id:
            products = products.filter(brand_id=brand_id)

        if id and slug:
            products = products.filter(
                Q(category__id=id, category__slug=slug) | Q(category2__id=id, category2__slug=slug) | Q(
                    category3__id=id, category3__slug=slug))

        if search_product := request.GET.get('search_product'):
            products = Product.objects.filter(name__contains=search_product)

        filter = ProductFilter(request.GET, queryset=products)
        products = filter.qs
        if not filter:
            return redirect('404.html')

        paginator = Paginator(products, 9)
        page = request.GET.get('page')
        products = paginator.get_page(page)
        url_data = request.GET.copy()
        if 'page' in url_data:
            del url_data['page']
        ctx = {
            'products': products,
            'filters': filter,
            'url_data': urlencode(url_data),
            # 'filter-brand':filter.get('brand'),
            'categories': Category.objects.filter(is_available=True),
            'categories2': CategorySecond.objects.filter(is_available=True),
            'categories3': CategorySub.objects.filter(is_available=True),

        }

        return render(request, self.template_name, ctx)


class AddToFavouriteProductView(LoginRequiredMixin, View):
    def get(self, request):
        # liked = False
        product = Product.objects.get(slug__exact=request.GET.get('p_slug'))
        obj, created = Like.objects.get_or_create(product=product, user=request.user)
        if created:
            liked = True
        else:
            obj.delete()
            liked = False
        data = {
            'liked': liked
        }
        return JsonResponse(data)


class AddToVarFavouriteProductView(LoginRequiredMixin,View):
    def get(self, request):
        # liked = False
        product = VariantProduct.objects.get(id=request.GET.get('p_id'))
        obj, created = Like.objects.get_or_create(var_product=product, user=request.user)
        if created:
            liked = True
        else:
            obj.delete()
            liked = False
        data = {
            'liked': liked
        }
        return JsonResponse(data)



class ProductDetailView(LoginRequiredMixin, View):
    template_name = 'products/ProductDetails.html'
    form_class = QuantityForm
    form_class_comment = CommentForm

    def setup(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, id=kwargs['id'], slug=kwargs['slug'])
        super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        product = self.product
        # selected_color = None

        selected_size = None
        if product.status == 'colorSize':
            selected_size = product.var_product.all().first()
        if selected_user := request.GET.get('Selected_Size'):
            selected_size = product.var_product.filter(id=selected_user).first()
        # colorSelect = request.GET.get('selected_color')
        # if product.status == 'colorSize' and not colorSelect:
        #     selected_color = product.var_product.all().first()
        #     selected_size = product.var_product.filter(color__id=selected_color.color.id)
        #     for s in selected_size:
        #         print(s.size.name)
        # colors = set()
        # variant_product = VariantProduct.objects.filter(product__id=product.id)
        # for v in variant_product:
        #     colors.add(v.color)
        product2 = product.tags.all()
        for i in product2:
            product2 = i.name
        product3 = Product.objects.filter(tags__name__icontains=product2)
        ip = get_client_ip(request)
        seen = SeenProduct(request)
        if len(seen) <= 10:
            seen.add(product=product)

        product2 = product.tags.all()
        for i in product2:
            product2 = i.name
        product3 = Product.objects.filter(tags__name__icontains=product2)
        ip = get_client_ip(request)
        comments = Comment.objects.filter(product=product, active=True, is_replay=False)
        # SizesOfColor = VariantProduct.objects.filter(product__id=product.id, color__id=colorSelect)
        ctx = {
            # 'selected_color': selected_color,
            # 'SizesOfColor': SizesOfColor,
            'selected_size':selected_size,
            'product3': product3,
            'product': product,
            'quantity': QuantityForm,
            # 'selected_size': selected_size,
            # 'colors': colors,
            # 'colors':unique_colors,
            # 'sizes': sizes,
            'comments': comments,
            'comment_Len': Comment.objects.filter(product_id=product.id, active=True).count(),
            'form_class_comment': self.form_class_comment,
        }
        return render(request, self.template_name, ctx)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        product = self.product
        form = self.form_class_comment(request.POST)
        if form.is_valid():
            com = form.save(commit=False)
            com.user = request.user
            com.product = product
            if comment_id := request.GET.get('cm_id'):
                replay_to = get_object_or_404(Comment, id=comment_id)
                com.replay_to = replay_to
                com.is_replay = True

            com.save()
            return redirect('Products:ProductDetails', product.id, product.slug)

        ctx = {
            'form': form
        }
        return render(request, self.template_name, ctx)


class AddToCompareView(LoginRequiredMixin, View):
    template_name = 'products/Compare.html'

    def get(self, request, category_id, id=None, p_slug=None):
        disable = False
        cat = Product.objects.filter(category2_id=category_id)
        compare = Compare(request)
        c_id = None
        c_cat_id = None
        for c in cat:
            c_id = c.id
            c_cat_id = c.category2
        if p_slug and category_id and not id:
            if product := Product.objects.get(slug=p_slug):
                compare = Compare(request)
                compare.clearCompare(request)
                compare.AddToCompare(product)
        if id and category_id:
            if product := Product.objects.get(id=id):
                compare = Compare(request)
                if len(compare) < 4:
                    compare.AddToCompare(product)
                    disable = False
                else:
                    disable = True
        if p_slug and category_id and id:
            if product := Product.objects.get(id=id):
                # print(request.session.get('Compare'))
                compare = Compare(request)
                print(len(compare))
                if len(compare) < 4:
                    print('hi')
                    compare.AddToCompare(product)
                    disable = False
                else:
                    print('ho')
                    disable = True
            cat = Product.objects.filter(category2_id=category_id)

            c_id = None
            c_cat_id = None
            for c in cat:
                c_id = c.id
                c_cat_id = c.category2
        ctx = {
            'compare': Compare(request),
            'products_fi': Product.objects.filter(category2_id=category_id).exclude(slug__in=compare),
            'c_id': c_id,
            'c_cat_id': c_cat_id,
            'disable': disable,
        }
        return render(request, self.template_name, ctx)


class CompareShowView(LoginRequiredMixin, View):
    template_name = 'products/Compare.html'

    def get(self, request):
        ctx = {
            'compare': Compare(request)
        }
        return render(request, self.template_name, ctx)


# class DeleteToCompareView(LoginRequiredMixin, View):
#     template_name = 'products/Compare.html'
#
#     def get(self, request):
#         p_slug = request.GET.get('c_slug')
#         category_id = request.GET.get('c_cat_two')
#         cat = Product.objects.filter(category2_id=category_id)
#         c_id = None
#         c_cat_id = None
#         for c in cat:
#             c_id = c.id
#             c_cat_id = c.category2
#         if product := Product.objects.get(slug=p_slug):
#             compare = Compare(request)
#             compare.remove(product)
#             if len(compare) == 0:
#                 compare.clearCompare(request)
#                 return redirect('Products:Products')
#             ctx = {
#                 'c_id': c_id,
#                 'c_cat_id': c_cat_id,
#                 'compare': Compare(request),
#                 'products_fi': Product.objects.filter(category2_id=category_id).exclude(slug__in=compare),
#             }
#             return render(request, self.template_name, ctx)
#
#         return HttpResponse('error')
class DeleteToCompareView(LoginRequiredMixin, View):
    template_name = 'products/Compare.html'

    def get(self, request):
        p_slug = request.GET.get('c_slug')
        category_id = request.GET.get('c_cat_two')
        cat = Product.objects.filter(category2_id=category_id)
        c_id = None
        c_cat_id = None
        for c in cat:
            c_id = c.id
            c_cat_id = c.category2
        if product := Product.objects.get(slug=p_slug):
            compare = Compare(request)
            compare.remove(product)
            if len(compare) == 0:
                compare.clearCompare(request)
                return redirect('Products:Products')
            ctx = {
                'c_id': c_id,
                'c_cat_id': c_cat_id,
                'compare': Compare(request),
                'products_fi': Product.objects.filter(category2_id=category_id).exclude(slug__in=compare),
            }
            return render(request, self.template_name, ctx)

        return HttpResponse('error')

#
#         # if not request.user.is_authenticated:
#         #     url = reverse('Accounts:Login')+ f'?next=products/details/{product.id}/{product.slug}'
#         #     return redirect(url)


# if color_name not in unique_colors:
#     unique_colors[color_name] = set()
# for size in p.size.all():
# sizes_for_color.append(size.name)
# print(size.name)

# unique_colors[color_name].add(size.name)
# ctx = {
#     'product3': product3,
#     'product': product,
#     'quantity': self.form_class(),
#     'colors': unique_colors,
#     # 'sizes':sizes_for_color,
# }
# return render(request, self.template_name, ctx)
# class AddToFavouriteProductView(LoginRequiredMixin, View):
#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             data = {
#                 'login_required': True
#
#             }
#             return JsonResponse(data)
#         return super().dispatch(request, *args, **kwargs)
#
#     def get(self, request):
#         product = Product.objects.get(slug__exact=request.GET.get('p_slug'))
#         obj, created = Like.objects.get_or_create(product=product, user=request.user)
#         if created:
#             liked = True
#         else:
#             liked = False
#             obj.delete()
#         data = {
#             'liked':liked
#         }
#         return JsonResponse(data)


# unique_colors = []
# sizes = []
# blue = request.GET.get('blue')
# if blue:
#     sizes = VariantProduct.objects.filter(color__name='blue')
#     for s in sizes:
#         print(s.name)

# comments = Comment.objects.filter(pro)

# colors = product.var_product.values_list('color__name','color__code').distinct()
# unique_colors = colors
#
# size = product.var_product.values_list('size__name',flat=True).distinct()
# sizes = size
# print(sizes)

# for s in c.var_size.all():
#     print(s.size.name)


# var_product = product.var_product.all()
# unique_colors = set(v.color for v in var_product)
# sizes = VariantProduct.objects.filter(product__id=product.id, color__id=v.color.id)
# print(unique_colors)

# if product.color.exists():
#     seen = SP(request)
#     res = seen.add(product=product)

# print(request.session.get('product_seen_id'))
