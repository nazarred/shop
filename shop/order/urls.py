from django.conf.urls import url
from order import views

urlpatterns = [

    url(r'^confirm/$', views.OrderConfirmView.as_view(), name='confirm'),
    url(r'^my-order/(?P<pk>\d+)/', views.UserOrdersView.as_view(), name='user_orders'),
    url(r'^my-order/detail/(?P<pk>\d+)/', views.UserOrderDetailView.as_view(), name='user_orders_detail'),

]
