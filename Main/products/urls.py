from  django.urls import path
from products import views

app_name = 'Products'

urlpatterns = [
    path('',views.ProductsView.as_view(),name='Products'),
    path('<int:id>/<slug>/', views.ProductsView.as_view(), name='Category_Product'),
    path('<int:brand_id>/',views.ProductsView.as_view(),name='Brand_Product'),



    path('LikeProd/', views.AddToFavouriteProductView.as_view(), name='Favourite'),
    path('LikeVarProd/', views.AddToVarFavouriteProductView.as_view(), name='VarProductFavourite'),

    path('compare/', views.CompareShowView.as_view(), name='CompareShow'),
    path('compare/<p_slug>/<category_id>/', views.AddToCompareView.as_view(), name='CompareAddPro'),
    path('compare/<int:id>/<category_id>/', views.AddToCompareView.as_view(), name='Compare'),
    path('compare/<int:id>/<category_id>/', views.AddToCompareView.as_view(), name='addProductCompare'),
    path('compare/<int:id>/<category_id>/<p_slug>/', views.AddToCompareView.as_view(), name='addProductsCompare'),


    path('compareDelete/', views.DeleteToCompareView.as_view(), name='CompareDelete'),
    path('Productdetails/<int:id>/<slug>/',views.ProductDetailView.as_view(),name='ProductDetails'),
]
#