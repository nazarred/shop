from django.conf.urls import url
from profile import views

urlpatterns = [

    url(r'^registration/$', views.RegisterView.as_view(), name='registration'),
    url(r'^detail/$', views.ProfileDetailView.as_view(), name='detail'),
    # url(r'^(?P<pk>\d+)/$', views.ProfileDetailView.as_view(), name='detail'),
    url(r'^update/(?P<pk>\d+)/$', views.ProfileUpdateView.as_view(), name='update'),
    url(r'^update/password/(?P<pk>\d+)/$', views.PasswordUpdateView.as_view(), name='update-password'),

]
