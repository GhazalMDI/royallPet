from django.contrib import admin

from products.models import *

class ExtraImageProductInline(admin.TabularInline):
    model = extraImage
    extra = 1

class VariantProductInline(admin.TabularInline):
    model = VariantProduct
    extra = 1

# class VariantProductSizeInline(admin.TabularInline):
#     model = VariantSize
#     extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','is_available','price','discount','total_sale')
    list_filter = ('is_available',)
    inlines = [ExtraImageProductInline,VariantProductInline]
    prepopulated_fields = {
        'slug':('name',)
    }
    # ExtraVariantInline
    readonly_fields = ('total_sale',)
    search_fields = ('name','is_available')
    # raw_id_fields = ('category','category2','category3')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug','is_available',)
    prepopulated_fields = {
        'slug':('name',)
    }
@admin.register(CategorySecond)
class CategorySecondAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_available','Parent_Cat')
    prepopulated_fields = {
        'slug': ('name',)
    }
@admin.register(CategorySub)
class CategorySubAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_available','Parent_Cat','Parent_Cat_two')
    prepopulated_fields = {
        'slug': ('name',)
    }

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user','body','active')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user','product','var_product')

admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Weight)
admin.site.register(Size)
admin.site.register(NewProduct)
# admin.site.register(SeenProduct)




# admin.site.register(VariantProduct)






