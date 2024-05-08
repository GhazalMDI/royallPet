from products.models import Category,Product,CategorySub,CategorySecond

def categoryFix(request):
     return {
        'categories': Category.objects.filter( is_available=True),
         'categories2': CategorySecond.objects.filter(is_available=True),
         'categories3': CategorySub.objects.filter(is_available=True),
         'products': Product.objects.filter(is_available=True),

    }