from django.conf.urls import include, url
from .views import views, control_views, training_views, demo_views, registration_login_views

urlpatterns = [
    # Examples:
    url(r'^results/save/', views.teachers_view_save, name='results_table_save'),
    url(r'^results/', views.teachers_view, name='results_table'),


    url(r'^control/properties/check', control_views.check_properties, name='control_check_properties'),
    url(r'^control/properties', control_views.properties, name='control_properties'),
    url(r'^control/matrix/check', control_views.matrix_check, name='control_check_matrix'),
    url(r'^control/matrix', control_views.matrix, name='control'),
    url(r'^control/warshalls/check', control_views.check_warshalls, name='control_warshalls_check'),
    url(r'^control/warshall', control_views.warshalls, name='control_warshalls'),
    url(r'^control/topological_sort/check', control_views.check_topological, name='control_topological_sort_check'),
    url(r'^control/topological_sort', control_views.topological, name='control_topological_sort'),



    url(r'^demo/', demo_views.demo, name='demo'),


    url(r'^training/warshalls/check', training_views.check_warshalls, name='training_check_warshalls'),
    url(r'^training/warshalls/', training_views.warshalls, name='training_warshalls'),

    url(r'^training/topological_sort/check', training_views.check_topological, name='train_topological_sort_check'),
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