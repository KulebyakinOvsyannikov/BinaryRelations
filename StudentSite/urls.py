from django.conf.urls import include, url
from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'BinaryRelations.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^control/check/', views.control_check, name='check_test'),
    url(r'^control/warshalls/check_tbls', views.control_warshalls_check_tables, name='control_warshalls_check_tables'),
    url(r'^control/warshalls/check', views.control_warshalls_check, name='control_warshalls_check'),
    url(r'^control/warshalls/', views.control_warshalls, name='control_warshalls'),
    url(r'^control/', views.control, name='control'),

    url(r'^demo/', views.demo, name='demo'),

    url(r'^training/check/', views.check_training, name='check_training'),
    url(r'^training/warshalls/check_tables', views.train_warshalls_check_tables, name='train_warshalls_check_tables'),
    url(r'^training/warshalls_tables/', views.train_warshalls_tables, name='train_warshalls_tables'),

    url(r'^training/warshalls/check', views.train_warshalls_check, name='train_warshalls_check'),
    url(r'^training/warshalls/', views.train_warshalls, name='train_warshalls'),

    url(r'^training/(?P<difficulty>easy|medium|hard)',
        views.training_with_difficulty,
        name='training_with_difficulty'
        ),
    url(r'^training/', views.training, name='training'),

    url(r'^registration/register', views.registration_action, name='registration_action'),
    url(r'^registration/', views.registration, name='registration'),

    url(r'^login/login-registration/', views.login_registration, name='login_registration'),
    url(r'^login/log', views.login_action, name='login_action'),
    url(r'^login/out', views.logout_action, name='logout_action'),
    url(r'^', views.index, name='index'),
]