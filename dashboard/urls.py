from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('apps.dashboard_app.urls')),
    url(r'^', include('apps.user_app.urls'))
]
