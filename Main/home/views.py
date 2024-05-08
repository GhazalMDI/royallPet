from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q

from home.models import Banner
from products.models import Product, NewProduct, Brand, Like,VariantProduct
from products.Seen_Product import SeenProduct
from utils import map_api
from home.forms import addressForm
import jdatetime
from django.http import JsonResponse


class homeView(View):
    template_name = 'home/home.html'
    form_class = addressForm

    def get(self, request):
        banners = Banner.objects.all()
        products = Product.objects.all()
        product = products.filter(slug=request.GET.get('p_slug')).first()
        # v_product = VariantProduct.objects.filter(slug=request.GET.get('p_slug')).first()

        # obj, created = Like.objects.get_or_create(product=product, user=request.user)
        # if created:
        #     liked = True
        #     print('hi')
        # else:
        #     obj.delete()
        #     liked = False
        #     print('bay')
        # data = {
        #     'liked': liked
        # }

        if search_box := request.GET.get('search_product'):
            products = Product.objects.filter(name__contains=search_box)
            if not products:
                return redirect('404.html')

        seen = SeenProduct(request)

        ctx = {
            # 'data':data,
            'seen': seen,
            'len_seen': len(seen),
            'banners': banners,
            'products': products,
            'form': self.form_class(),
            'new_prod': NewProduct.objects.all(),
            'product_cat': Product.objects.filter(category__name='گربه'),
            'product_dog': Product.objects.filter(category__name='سگ'),
            'brands': Brand.objects.all()[:10]
        }
        return render(request, self.template_name, ctx)

    def post(self, request):
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        location = map_api.map(lat, lng)
        banners = Banner.objects.all()
        products = Product.objects.all()
        ctx = {
            'seen': SeenProduct(request),
            'banners': banners,
            'products': products,
            'form': self.form_class(),
            'location': location,
            'new_prod': NewProduct.objects.all()[:10],
            'product_cat': Product.objects.filter(category__name='گربه'),
            'product_dog': Product.objects.filter(category__name='سگ')
        }
        return render(request, self.template_name, ctx)
        # form = self.form_class(request.POST)
        # if form.is_valid():
        #     cd = form.cleaned_data
        #     loc1 = map_api.geocodingMap(cd.get('location'))
        #     latitude = loc1['location']['x']
        #     longitude = loc1['location']['y']
        #     ctx = {
        #         'latitude': latitude,
        #         'longitude': longitude,
        #         'form': self.form_class()
        #     }
        #     return render(request, self.template_name, ctx)

    # form = self.form_class(request.POST)
    # if form.is_valid():
    #     cd = form.cleaned_data
    #     location1 = map_api.geocodingMap(cd.get('location'))
    #     print(location1)
    #     ctx = {
    #         'form': self.form_class(),
    # 'address_x':location.get('x')
    # }
    #     return render(request,self.template_name,ctx)
    # ctx = {
    #     'form':form
    # }
    # return render(request,self.template_name,ctx)
