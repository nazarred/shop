from django.conf.urls import url
from profile import views

urlpatterns = [
    url(r'^profile/$', views.ProfileDetailView.as_view(), name='detail'),
    url(r'^update/$', views.ProfileUpdateView.as_view(), name='update'),
]
