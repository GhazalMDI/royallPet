from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Product, NewProduct


@receiver(post_save, sender=Product)
def AddToTenNewProductHandler(**kwargs):
    product = kwargs['instance']
    if kwargs['created']:
        if NewProduct.objects.count() > 10:
            NewProduct.objects.all().order_by('id')[0].delete()
            # NewProduct.objects.create(product=product)
        NewProduct.objects.create(product=product)
