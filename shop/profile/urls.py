from django.conf.urls import url
from profile import views

urlpatterns = [

    url(r'^registration/$', views.RegisterView.as_view(), name='registration'),
]
