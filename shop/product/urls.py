from django.conf.urls import url
from product import views

urlpatterns = [

    url(r'^detail/(?P<pk>\d+)/', views.ProductDetailView.as_view(), name='product_detail'),
    url(r'^rating_change/(?P<pk>\d+)/', views.rating_change, name='rating_change'),
    url(r'^comments/(?P<pk>\d+)/', views.comments, name='comments'),

]
