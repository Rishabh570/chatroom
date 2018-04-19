from django.conf.urls import url
from chatapp import views


urlpatterns = [
    url('^list/', views.user_list, name='list'),
    url('signup/', views.sign_up, name='sign_up'),
    url('login/', views.log_in, name='log_in'),
    url('logout/', views.log_out, name='log_out'),

]
