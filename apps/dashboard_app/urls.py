from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='dashboard_index'),
    url(r'^home$', views.home, name='dashboard_home'),
    url(r'^user/(?P<user_id>\d+)/edit$', views.edit),
    url(r'^user/(?P<user_id>\d+)/board$', views.board),
    url(r'^board/(?P<board_id>\d+)/post$', views.post),
    url(r'^board/(?P<post_id>\d+)/comment$', views.comment)
]
