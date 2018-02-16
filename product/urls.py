from django.conf.urls import url
from product import views

urlpatterns = [

    url(r'^detail/(?P<pk>\d+)/', views.product_detail, name='product_detail'),
]
