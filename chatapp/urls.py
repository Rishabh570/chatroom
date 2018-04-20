from django.conf.urls import url
from chatapp import views

app_name = "chatapp"
urlpatterns = [
    url(r'^list/$', views.list, name='list'),
    url(r'^signup/$', views.sign_up, name='sign_up'),
    url(r'^login/$', views.log_in, name='log_in'),
    url(r'^logout/$', views.log_out, name='log_out'),

]
