from django.urls import path

from cart import views

app_name = 'cart'

urlpatterns = [
    # path('cart/',views.CartView.as_view(),name='Cart'),

    path('AddToCart/', views.AddToCartView.as_view(), name='CartAdd'),
    path('AddToVariantCart/', views.AddToVariantCartView.as_view(), name='VariantCartAdd'),
    path('AddToVariantLikeCart/', views.AddToVariantLikeCartView.as_view(), name='AddToVariantLikeCartView'),

    path('AddToCartFromLike/<int:c_id>/', views.AddToCartFromLikeView.as_view(), name='CartAddLike'),
    path('AddToVariantCartFromLike/<int:c_id>/', views.AddToVaraintCartFromLikeView.as_view(), name='CartVarAddLike'),

    path('LikedProd/Delete/',views.RemoveTofavouriteView.as_view(),name='DeleteFavourite'),
    path('LikedVarProd/Delete/', views.RemoveToVarfavouriteView.as_view(), name='DeleteVarFavourite'),

    path('AddOneToCart/',views.AddOneToCartView.as_view(),name='CartOneAdd'),
    path('AddOneToVarCart/', views.AddOneToVarCartView.as_view(), name='VarCartOneAdd'),

    path('DeleteOneToCart/', views.DeleteOneToCartView.as_view(), name='CartOneDelete'),
    path('DeleteVar/', views.DeleteVariantProduct.as_view(), name='deleteVar'),


    path('RemoveProduct/',views.RemoveProduct.as_view(),name='RemoveCartProduct'),
    path('RemoveVarProduct/', views.RemoveVarProduct.as_view(), name='RemoveCartVarProduct')

]
