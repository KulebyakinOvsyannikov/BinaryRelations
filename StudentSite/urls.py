from django.conf.urls import include, url
from .views import views, control_views, training_views, demo_views, registration_login_views

urlpatterns = [
    # Examples:
    url(r'^control/check/', control_views.control_check, name='check_test'),
    url(r'^control/warshalls/check', control_views.control_warshalls_check, name='control_warshalls_check'),
    url(r'^control/warshalls/', control_views.control_warshalls, name='control_warshalls'),
    url(r'^control/topological_sort/check', control_views.control_topological_check, name='control_topological_sort_check'),
    url(r'^control/topological_sort', control_views.control_topological, name='control_topological_sort'),

    url(r'^control/', control_views.control, name='control'),

    url(r'^demo/', demo_views.demo, name='demo'),

    url(r'^training/check/', training_views.check_training, name='check_training'),

    url(r'^training/warshalls/check', training_views.check_warshalls, name='training_check_warshalls'),
    url(r'^training/warshalls/', training_views.warshalls, name='training_warshalls'),

    url(r'^training/topological_sort/check', training_views.train_topological_check, name='train_topological_sort_check'),
    url(r'^training/topological_sort', training_views.topological, name='training_topological'),
    url(r'^training/properties/check', training_views.check_properties, name='training_check_properties'),
    url(r'^training/properties', training_views.properties, name='training_properties'),
    url(r'^training/matrix/check', training_views.check_matrix, name='training_check_matrix'),

    url(r'^training/(?P<difficulty>easy|medium|hard)',
        training_views.training_with_difficulty,
        name='training_with_difficulty'
        ),
    url(r'^training/', training_views.training, name='training'),

    url(r'^registration/register', registration_login_views.registration_action, name='registration_action'),
    url(r'^registration/', registration_login_views.registration, name='registration'),

    url(r'^login/login-registration/', registration_login_views.login_registration, name='login_registration'),
    url(r'^login/log', registration_login_views.login_action, name='login_action'),
    url(r'^login/out', registration_login_views.logout_action, name='logout_action'),
    url(r'^', views.index, name='index'),
]