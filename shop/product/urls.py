from django.conf.urls import url
from product import views

urlpatterns = [

    url(r'^detail/(?P<pk>\d+)/', views.product_detail, name='product_detail'),
    url(r'^rating_change/(?P<pk>\d+)/', views.rating_change, name='rating_change'),

]
