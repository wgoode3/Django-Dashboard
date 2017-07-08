from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register$', views.register, name='user_register'),
    url(r'^login$', views.login, name='user_login'),
    url(r'^logout$', views.logout, name='user_logout'),
    url(r'^user/(?P<user_id>\d+)/update', views.update),
    url(r'^user/(?P<user_id>\d+)/change_pass', views.change_pass),
    url(r'^user/(?P<user_id>\d+)/change_level', views.change_level),
    url(r'^user/(?P<user_id>\d+)/delete', views.delete)
]