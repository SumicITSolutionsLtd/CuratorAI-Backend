"""
URL patterns for test dashboard.
"""
from django.urls import path
from .views import (
    test_dashboard,
    run_all_tests,
    run_module_tests,
    run_single_test,
    get_test_list,
    get_endpoints,
    test_endpoint,
    create_test_user,
)

app_name = 'test_dashboard'

urlpatterns = [
    path('', test_dashboard, name='dashboard'),
    path('api/run-all/', run_all_tests, name='run-all'),
    path('api/run-module/', run_module_tests, name='run-module'),
    path('api/run-test/', run_single_test, name='run-test'),
    path('api/tests/', get_test_list, name='test-list'),
    path('api/endpoints/', get_endpoints, name='endpoints'),
    path('api/test-endpoint/', test_endpoint, name='test-endpoint'),
    path('api/create-test-user/', create_test_user, name='create-test-user'),
]

