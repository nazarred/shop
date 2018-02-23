from django.conf.urls import url

from src.product import views

urlpatterns = [

    url(r'^detail/(?P<pk>\d+)/', views.product_detail, name='product_detail'),
    url(r'^rating_change/', views.rating_change, name='rating_change'),

]
