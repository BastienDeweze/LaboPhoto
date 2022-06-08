from django.urls import path
from .views import Store, ProductDetail, SearchStore, ChangeSize, ChangeColor

app_name = 'store'

urlpatterns = [
    path('', Store.as_view(), name="store"),
    path('category/<slug:category_slug>/', Store.as_view(), name="product_by_category"),
    path('detail/<slug:slug>/', ProductDetail.as_view(), name="product_detail"),
    path('search/', SearchStore.as_view(), name="search"),
    path('changesizesearch/<int:size>/', ChangeSize.as_view(), name="sizesearch"),
    path('changecolorsearch/<int:color>/', ChangeColor.as_view(), name="colorsearch"),
]
