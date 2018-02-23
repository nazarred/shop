from django.conf.urls import url

from src.profile import views

urlpatterns = [

    url(r'^registration$', views.register, name='registration'),
    # url(r'^(?P<pk>\d+)/', views.user_detail, name='user_detail'),
]
