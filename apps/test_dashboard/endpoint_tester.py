"""
Endpoint testing utility for discovering and testing API endpoints.
"""
import json
import logging
import traceback
from typing import Dict, List, Optional, Any
from django.urls import get_resolver
from django.conf import settings
from django.test import Client, override_settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
import io
import sys

User = get_user_model()

# Set up logging to capture debug information
logger = logging.getLogger(__name__)


class EndpointDiscovery:
    """Discover all API endpoints in the application."""
    
    def __init__(self):
        self.endpoints = []
        self.base_url = '/api/v1'
    
    def discover_endpoints(self) -> List[Dict]:
        """Discover all API endpoints."""
        from django.urls import reverse
        resolver = get_resolver()
        
        # Start from root URLconf
        try:
            self._extract_urls(resolver.url_patterns, prefix='')
        except Exception as e:
            # Fallback: manually list known endpoints
            self._add_known_endpoints()
        
        # Remove duplicates and sort
        seen = set()
        unique_endpoints = []
        for ep in self.endpoints:
            key = (ep['path'], tuple(ep['methods']))
            if key not in seen:
                seen.add(key)
                unique_endpoints.append(ep)
        
        return sorted(unique_endpoints, key=lambda x: (x['category'], x['path']))
    
    def _add_known_endpoints(self):
        """Add known endpoints as fallback."""
        # This is a comprehensive list of actual endpoints
        known_endpoints = [
            # Authentication
            {'path': '/api/v1/auth/register/', 'methods': ['POST'], 'category': 'Authentication', 'description': 'Register new user'},
            {'path': '/api/v1/auth/login/', 'methods': ['POST'], 'category': 'Authentication', 'description': 'User login'},
            {'path': '/api/v1/auth/logout/', 'methods': ['POST'], 'category': 'Authentication', 'description': 'User logout'},
            {'path': '/api/v1/auth/me/', 'methods': ['GET', 'PUT', 'PATCH'], 'category': 'Authentication', 'description': 'Get or update current user profile'},
            {'path': '/api/v1/auth/refresh/', 'methods': ['POST'], 'category': 'Authentication', 'description': 'Refresh JWT token'},
            {'path': '/api/v1/auth/users/<pk>/', 'methods': ['GET'], 'category': 'Authentication', 'description': 'Get user details by ID'},
            {'path': '/api/v1/auth/users/search/', 'methods': ['GET'], 'category': 'Authentication', 'description': 'Search users'},
            # Outfits
            {'path': '/api/v1/outfits/', 'methods': ['GET', 'POST'], 'category': 'Outfits', 'description': 'List or create outfits'},
            {'path': '/api/v1/outfits/<pk>/', 'methods': ['GET', 'PUT', 'PATCH', 'DELETE'], 'category': 'Outfits', 'description': 'Get, update, or delete outfit'},
            # Social Feed
            {'path': '/api/v1/social/feed/', 'methods': ['GET'], 'category': 'Social Feed', 'description': 'Get social feed'},
            {'path': '/api/v1/social/posts/', 'methods': ['POST'], 'category': 'Social Feed', 'description': 'Create a new post'},
            {'path': '/api/v1/social/posts/<pk>/', 'methods': ['GET'], 'category': 'Social Feed', 'description': 'Get post details'},
            # Lookbooks
            {'path': '/api/v1/lookbooks/', 'methods': ['GET'], 'category': 'Lookbooks', 'description': 'List lookbooks'},
            {'path': '/api/v1/lookbooks/create/', 'methods': ['POST'], 'category': 'Lookbooks', 'description': 'Create a new lookbook'},
            {'path': '/api/v1/lookbooks/<pk>/', 'methods': ['GET'], 'category': 'Lookbooks', 'description': 'Get lookbook details'},
        ]
        self.endpoints.extend(known_endpoints)
    
    def _extract_urls(self, patterns, prefix=''):
        """Recursively extract URL patterns."""
        for pattern in patterns:
            try:
                if hasattr(pattern, 'url_patterns'):
                    # This is an include
                    new_prefix = prefix + str(pattern.pattern)
                    self._extract_urls(pattern.url_patterns, new_prefix)
                else:
                    # This is a URL pattern
                    url_pattern = str(pattern.pattern)
                    # Keep parameter names for better readability but format nicely
                    # Replace <int:pk> with <pk>, <str:slug> with <slug>, etc.
                    import re
                    display_pattern = re.sub(r'<(int|str|slug|uuid|path):(\w+)>', r'<\2>', url_pattern)
                    full_path = (prefix + display_pattern).replace('//', '/')
                    
                    # Only include API v1 endpoints
                    if '/api/v1' in full_path or full_path.startswith('api/v1') or full_path.startswith('/api/v1'):
                        # Normalize path
                        if not full_path.startswith('/'):
                            full_path = '/' + full_path
                        
                        # Get allowed methods from view if available
                        methods = self._get_allowed_methods(pattern)
                        
                        endpoint_info = {
                            'path': full_path,
                            'name': getattr(pattern, 'name', ''),
                            'methods': methods,
                            'description': self._get_endpoint_description(pattern),
                            'category': self._categorize_endpoint(full_path),
                        }
                        self.endpoints.append(endpoint_info)
            except Exception as e:
                # Skip patterns that can't be processed
                continue
    
    def _get_allowed_methods(self, pattern) -> List[str]:
        """Get allowed HTTP methods for an endpoint."""
        try:
            if hasattr(pattern, 'callback'):
                view = pattern.callback
                view_class = None
                
                # Try to get the view class
                if hasattr(view, 'cls'):
                    view_class = view.cls
                elif hasattr(view, 'view_class'):
                    view_class = view.view_class
                elif callable(view) and hasattr(view, '__self__'):
                    # It's a bound method
                    view_class = view.__self__.__class__
                
                if view_class:
                    # Check for DRF APIView or ViewSet
                    if hasattr(view_class, 'http_method_names'):
                        methods = [m.upper() for m in view_class.http_method_names if m.upper() not in ['OPTIONS', 'HEAD', 'TRACE']]
                        if methods:
                            return methods
                    elif hasattr(view_class, 'allowed_methods'):
                        methods = [m for m in view_class.allowed_methods if m not in ['OPTIONS', 'HEAD', 'TRACE']]
                        if methods:
                            return methods
                    
                    # Check for specific methods in the class
                    common_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
                    available_methods = []
                    for method in common_methods:
                        if hasattr(view_class, method.lower()) or hasattr(view_class, method.lower() + '_method'):
                            available_methods.append(method)
                    
                    if available_methods:
                        return available_methods
        except Exception:
            pass
        
        # Default: try to infer from common patterns
        # If it's a detail view (has <int:pk> or similar), likely GET, PUT, PATCH, DELETE
        # If it's a list view, likely GET, POST
        return ['GET', 'POST']
    
    def _get_endpoint_description(self, pattern) -> str:
        """Get description from view if available."""
        if hasattr(pattern, 'callback'):
            view = pattern.callback
            if hasattr(view, 'cls'):
                view_class = view.cls
                if hasattr(view_class, '__doc__') and view_class.__doc__:
                    return view_class.__doc__.strip().split('\n')[0]
        return ''
    
    def _categorize_endpoint(self, path: str) -> str:
        """Categorize endpoint based on path."""
        if '/auth/' in path:
            return 'Authentication'
        elif '/outfits/' in path:
            return 'Outfits'
        elif '/wardrobe/' in path:
            return 'Wardrobe'
        elif '/social/' in path:
            return 'Social Feed'
        elif '/lookbooks/' in path:
            return 'Lookbooks'
        elif '/cart/' in path:
            return 'Shopping Cart'
        elif '/notifications/' in path:
            return 'Notifications'
        else:
            return 'Other'


class EndpointTester:
    """Test API endpoints with detailed logging."""
    
    def __init__(self):
        # Use APIClient which bypasses middleware and doesn't require ALLOWED_HOSTS
        # APIClient is a test client that doesn't go through normal HTTP stack
        self.client = APIClient()
        self.logs = []
        self.request_log = {}
        self.response_log = {}
    
    def _replace_url_params(self, path: str) -> str:
        """Replace URL parameters with example values."""
        import re
        # Replace <int:pk> or <pk> with 1
        path = re.sub(r'<int:\w+>', '1', path)
        path = re.sub(r'<str:\w+>', 'example', path)
        path = re.sub(r'<slug:\w+>', 'example-slug', path)
        path = re.sub(r'<uuid:\w+>', '00000000-0000-0000-0000-000000000000', path)
        path = re.sub(r'<path:\w+>', 'example/path', path)
        # Replace any remaining <...> patterns (like <pk>, <id>, etc.)
        # Common parameter names and their defaults
        param_defaults = {
            'pk': '1',
            'id': '1',
            'user_id': '1',
            'post_id': '1',
            'lookbook_id': '1',
            'outfit_id': '1',
            'item_id': '1',
            'notification_id': '1',
            'comment_id': '1',
        }
        for param_name, default_value in param_defaults.items():
            path = re.sub(f'<{param_name}>', default_value, path)
        # Replace any remaining <...> with 1
        path = re.sub(r'<\w+>', '1', path)
        return path
    
    def test_endpoint(
        self,
        method: str,
        path: str,
        data: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        auth_token: Optional[str] = None,
        user_id: Optional[int] = None
    ) -> Dict:
        """
        Test an API endpoint with detailed logging.
        
        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            path: API endpoint path
            data: Request body data
            headers: Additional headers
            auth_token: JWT token for authentication
            user_id: User ID to authenticate as (creates token if not provided)
        
        Returns:
            Detailed test results including request, response, and logs
        """
        self.logs = []
        self.request_log = {}
        self.response_log = {}
        
        # Clear any previous credentials
        self.client.credentials()
        
        # Set up authentication if needed
        if auth_token:
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {auth_token}')
        elif user_id:
            try:
                user = User.objects.get(id=user_id)
                refresh = RefreshToken.for_user(user)
                token = str(refresh.access_token)
                self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
                self._log('info', f'Authenticated as user ID {user_id} (email: {user.email})')
            except User.DoesNotExist:
                self._log('warning', f'User with ID {user_id} not found, proceeding without authentication')
        
        # Replace URL parameters if needed
        actual_path = self._replace_url_params(path)
        
        # Prepare request
        request_data = {
            'method': method.upper(),
            'path': path,
            'actual_path': actual_path,
            'data': data or {},
            'headers': headers or {},
        }
        
        # Add authentication header to request log
        if auth_token or user_id:
            auth_header = self.client._credentials.get('HTTP_AUTHORIZATION', '')
            if auth_header:
                request_data['headers']['Authorization'] = auth_header[:50] + '...' if len(auth_header) > 50 else auth_header
        
        self.request_log = request_data
        self._log('info', f'Preparing {method.upper()} request to {path}')
        
        # Capture stdout/stderr for debugging
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        try:
            sys.stdout = stdout_capture
            sys.stderr = stderr_capture
            
            # Use override_settings to bypass ALLOWED_HOSTS check for testing
            # We use 'testserver' which is Django's default test host
            # This is safe because:
            # 1. It only affects requests within this context manager
            # 2. The test client doesn't make real HTTP requests
            # 3. We're using a specific test host, not '*'
            # 4. This only runs in the test dashboard, not in production API calls
            test_hosts = list(settings.ALLOWED_HOSTS) + ['testserver', 'localhost', '127.0.0.1']
            with override_settings(ALLOWED_HOSTS=test_hosts, SERVER_NAME='testserver'):
                # Make the request using APIClient (test client)
                method_func = getattr(self.client, method.lower())
                
                # Use actual_path for the request
                # Convert headers to HTTP_ format for Django test client
                request_headers = {}
                if headers:
                    for k, v in headers.items():
                        header_name = 'HTTP_' + k.upper().replace('-', '_')
                        request_headers[header_name] = v
                
                # Ensure Content-Type is set for POST/PUT/PATCH
                if method.upper() in ['POST', 'PUT', 'PATCH'] and data:
                    request_headers['HTTP_CONTENT_TYPE'] = 'application/json'
                
                # Make the request
                if data and method.upper() not in ['GET', 'HEAD']:
                    response = method_func(actual_path, data, format='json', **request_headers)
                else:
                    # For GET/HEAD/DELETE, data goes as query params
                    if data and method.upper() in ['GET', 'HEAD']:
                        response = method_func(actual_path, data, format='json', **request_headers)
                    else:
                        response = method_func(actual_path, format='json', **request_headers)
            
            # Capture response
            try:
                # Try to get response.data (DRF response)
                if hasattr(response, 'data'):
                    response_data = response.data
                else:
                    # Fall back to parsing content
                    content = response.content.decode('utf-8') if hasattr(response, 'content') else ''
                    if content:
                        try:
                            import json
                            response_data = json.loads(content)
                        except:
                            response_data = {'raw_content': content[:1000]}
                    else:
                        response_data = {}
            except Exception as e:
                # If response.data fails, try to parse JSON from content
                try:
                    import json
                    content = response.content.decode('utf-8') if hasattr(response, 'content') else ''
                    if content:
                        try:
                            response_data = json.loads(content)
                        except json.JSONDecodeError:
                            # Check if it's an HTML error page
                            if 'DisallowedHost' in content or 'disallowed' in content.lower():
                                response_data = {
                                    'error': 'DisallowedHost error',
                                    'message': 'The request was blocked by Django\'s ALLOWED_HOSTS setting. This should not happen with the test client.',
                                    'suggestion': 'This is likely a configuration issue. The APIClient should bypass this check.'
                                }
                            else:
                                response_data = {'raw_content': content[:1000], 'parse_error': str(e)}
                    else:
                        response_data = {'error': 'Could not parse response', 'parse_error': str(e)}
                except:
                    response_data = {'error': 'Could not parse response', 'parse_error': str(e)}
            
            # Get response content
            content = ''
            if hasattr(response, 'content'):
                try:
                    content = response.content.decode('utf-8')
                except:
                    content = str(response.content)
            
            # Check content type
            content_type = response.get('Content-Type', '') if hasattr(response, 'get') else ''
            is_json = 'application/json' in content_type.lower()
            
            # Try to parse as JSON
            parsed_content = response_data
            if content and (not response_data or response_data == {}):
                try:
                    import json
                    # Try to parse JSON
                    if is_json or (content.strip().startswith('{') or content.strip().startswith('[')):
                        parsed_content = json.loads(content)
                        response_data = parsed_content
                    else:
                        # Might be HTML error page, try to extract error info
                        parsed_content = {'raw_content': content[:500]}  # Limit size
                except json.JSONDecodeError:
                    # Not JSON, might be HTML
                    if '<html' in content.lower() or '<body' in content.lower():
                        # Extract error message from HTML if possible
                        import re
                        error_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
                        if error_match:
                            parsed_content = {'error': error_match.group(1), 'content_type': 'html'}
                        else:
                            parsed_content = {'raw_content': content[:500]}
                    else:
                        parsed_content = {'raw_content': content[:500]}
            
            self.response_log = {
                'status_code': response.status_code,
                'status_text': self._get_status_text(response.status_code),
                'headers': dict(response.items()),
                'data': response_data,
                'content': content,
                'parsed_content': parsed_content if isinstance(parsed_content, dict) else None,
            }
            
            self._log('info', f'Received response: {response.status_code} {self._get_status_text(response.status_code)}')
            
        except Exception as e:
            error_trace = traceback.format_exc()
            self._log('error', f'Error making request: {str(e)}')
            self._log('error', f'Traceback:\n{error_trace}')
            
            # Try to extract more info from the error
            error_msg = str(e)
            if 'DisallowedHost' in error_msg or 'disallowed' in error_msg.lower():
                error_msg += ' (Note: This should not happen with APIClient. The test client bypasses ALLOWED_HOSTS checks.)'
            
            self.response_log = {
                'status_code': 500,
                'status_text': 'Internal Server Error',
                'error': error_msg,
                'traceback': error_trace,
                'data': {'error': error_msg, 'type': type(e).__name__},
                'content': error_trace,
            }
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
        
        # Capture logs
        stdout_content = stdout_capture.getvalue()
        stderr_content = stderr_capture.getvalue()
        
        # Build result
        result = {
            'success': self.response_log.get('status_code', 0) < 400 if 'status_code' in self.response_log else False,
            'request': self.request_log,
            'response': self.response_log,
            'logs': self.logs,
            'stdout': stdout_content,
            'stderr': stderr_content,
            'summary': self._generate_summary(),
        }
        
        return result
    
    def _log(self, level: str, message: str):
        """Add a log entry."""
        self.logs.append({
            'level': level,
            'message': message,
            'timestamp': self._get_timestamp(),
        })
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from django.utils import timezone
        return timezone.now().isoformat()
    
    def _get_status_text(self, status_code: int) -> str:
        """Get human-readable status text."""
        status_map = {
            200: 'OK',
            201: 'Created',
            204: 'No Content',
            400: 'Bad Request',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not Found',
            500: 'Internal Server Error',
        }
        return status_map.get(status_code, 'Unknown')
    
    def _generate_summary(self) -> Dict:
        """Generate a human-readable summary."""
        summary = {
            'for_frontend': '',
            'for_backend': '',
            'for_layman': '',
        }
        
        status_code = self.response_log.get('status_code', 0)
        method = self.request_log.get('method', '')
        path = self.request_log.get('path', '')
        
        # Frontend summary
        if status_code < 400:
            summary['for_frontend'] = f'✅ Success! The {method} request to {path} returned status {status_code}. You can use this endpoint in your frontend application.'
        else:
            summary['for_frontend'] = f'❌ Error! The {method} request to {path} failed with status {status_code}. Check the error details in the response.'
        
        # Backend summary
        if status_code < 400:
            data_keys = list(self.response_log.get("data", {}).keys())
            summary['for_backend'] = f'Endpoint {path} responded successfully with status {status_code}. Response data structure: {data_keys if data_keys else "Empty response"}'
        else:
            error_data = self.response_log.get('data', {}) or self.response_log.get('parsed_content', {}) or {}
            error_details = error_data.get('error', error_data.get('details', error_data.get('message', error_data)))
            if not error_details:
                error_details = error_data
            summary['for_backend'] = f'Endpoint {path} returned error {status_code}. Error details: {error_details}'
        
        # Layman summary
        if status_code < 400:
            summary['for_layman'] = f'Great! The request was successful. The server understood what you asked for and responded correctly.'
        else:
            summary['for_layman'] = f'Something went wrong. The server returned an error code {status_code}. This usually means the request was missing some information or there was a problem processing it.'
        
        return summary

