from django.conf.urls import url
from product import views

urlpatterns = [

    url(r'^detail/(?P<pk>\d+)/', views.ProductDetailView.as_view(), name='product_detail'),
    url(r'^rating_change/(?P<pk>\d+)/', views.rating_change, name='rating_change'),
    url(r'^comments/(?P<pk>\d+)/', views.comments, name='comments'),
    url(r'^add_product_in_cart/(?P<pk>\d+)/', views.add_product_in_cart, name='add_product_in_cart'),
    url(r'^product_in_cart/$', views.ProductsCartView.as_view(), name='product_in_cart'),
    url(r'^delete_product_from_cart/(?P<pk>\d+)/$', views.DeleteProductsFromCartView.as_view(),
        name='delete_product_from_cart'),
]
