"""
Test dashboard views for running and viewing test results.
"""
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from core.test_runner import TestRunner
from .endpoint_tester import EndpointDiscovery, EndpointTester
from pathlib import Path


def test_dashboard(request):
    """Render test dashboard page."""
    runner = TestRunner()
    test_list = runner.get_test_list()
    
    # Group tests by module
    tests_by_module = {}
    for test in test_list:
        module = test['module']
        if module not in tests_by_module:
            tests_by_module[module] = []
        tests_by_module[module].append(test)
    
    context = {
        'tests_by_module': tests_by_module,
        'total_tests': len(test_list)
    }
    
    return render(request, 'test_dashboard.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def run_all_tests(request):
    """API endpoint to run all tests."""
    runner = TestRunner()
    results = runner.run_all_tests()
    return JsonResponse(results)


@csrf_exempt
@require_http_methods(["POST"])
def run_module_tests(request):
    """API endpoint to run tests for a specific module."""
    module = request.POST.get('module') or request.body.decode('utf-8')
    if isinstance(module, str) and module.startswith('{'):
        try:
            data = json.loads(module)
            module = data.get('module')
        except:
            pass
    
    if not module:
        return JsonResponse({'error': 'Module name required'}, status=400)
    
    runner = TestRunner()
    results = runner.run_test_module(module)
    return JsonResponse(results)


@csrf_exempt
@require_http_methods(["POST"])
def run_single_test(request):
    """API endpoint to run a single test."""
    test_path = request.POST.get('test_path') or request.body.decode('utf-8')
    if isinstance(test_path, str) and test_path.startswith('{'):
        try:
            data = json.loads(test_path)
            test_path = data.get('test_path')
        except:
            pass
    
    if not test_path:
        return JsonResponse({'error': 'Test path required'}, status=400)
    
    runner = TestRunner()
    results = runner.run_single_test(test_path)
    return JsonResponse(results)


@require_http_methods(["GET"])
def get_test_list(request):
    """API endpoint to get list of all tests."""
    runner = TestRunner()
    test_list = runner.get_test_list()
    return JsonResponse({'tests': test_list})


@require_http_methods(["GET"])
def get_endpoints(request):
    """API endpoint to get list of all API endpoints."""
    discovery = EndpointDiscovery()
    endpoints = discovery.discover_endpoints()
    return JsonResponse({'endpoints': endpoints})


@csrf_exempt
@require_http_methods(["POST"])
def test_endpoint(request):
    """API endpoint to test a single API endpoint."""
    try:
        data = json.loads(request.body.decode('utf-8'))
        
        method = data.get('method', 'GET')
        path = data.get('path', '')
        request_data = data.get('data', {})
        headers = data.get('headers', {})
        auth_token = data.get('auth_token', '')
        user_id = data.get('user_id')
        
        if not path:
            return JsonResponse({'error': 'Path is required'}, status=400)
        
        tester = EndpointTester()
        result = tester.test_endpoint(
            method=method,
            path=path,
            data=request_data,
            headers=headers,
            auth_token=auth_token,
            user_id=user_id
        )
        
        return JsonResponse(result)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def create_test_user(request):
    """Create a test user and return JWT token."""
    from django.contrib.auth import get_user_model
    from apps.accounts.models import UserProfile, StylePreference
    from rest_framework_simplejwt.tokens import RefreshToken
    
    User = get_user_model()
    
    try:
        # Create or get test user
        user, created = User.objects.get_or_create(
            email='test@example.com',
            defaults={
                'username': 'testuser',
                'password': 'pbkdf2_sha256$600000$dummy$dummy=',  # Will be set properly
                'first_name': 'Test',
                'last_name': 'User',
            }
        )
        
        if created:
            user.set_password('testpass123')
            user.save()
            # Create related objects
            UserProfile.objects.get_or_create(user=user)
            StylePreference.objects.get_or_create(user=user)
        else:
            # Ensure password is correct
            if not user.check_password('testpass123'):
                user.set_password('testpass123')
                user.save()
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return JsonResponse({
            'success': True,
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
            },
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

