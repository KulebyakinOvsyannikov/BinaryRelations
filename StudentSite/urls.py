from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'BinaryRelations.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^login/', views.login_view, name='login_action'),
    url(r'^logout/', views.logout_view, name='logout_action'),
    url(r'^test/', views.test_view, name='test_view'),
    url(r'^check_test_task/', views.check_test_task, name='check_test_view'),
    url(r'^', views.index_view, name='index_view'),
]