"""
Custom exception handlers for CuratorAI API.
"""
import uuid
from datetime import datetime
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import (
    ValidationError,
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
    NotFound,
    MethodNotAllowed,
    Throttled,
)
from django.http import Http404
from django.core.exceptions import ValidationError as DjangoValidationError


def get_error_code(exc, status_code):
    """
    Map exception types and status codes to error codes.
    """
    error_code_mapping = {
        status.HTTP_400_BAD_REQUEST: {
            ValidationError: 'VALIDATION_ERROR',
            DjangoValidationError: 'VALIDATION_ERROR',
            'default': 'BAD_REQUEST'
        },
        status.HTTP_401_UNAUTHORIZED: {
            AuthenticationFailed: 'AUTH_INVALID_CREDENTIALS',
            NotAuthenticated: 'AUTH_INVALID_TOKEN',
            'default': 'UNAUTHORIZED'
        },
        status.HTTP_403_FORBIDDEN: {
            PermissionDenied: 'PERMISSION_DENIED',
            'default': 'FORBIDDEN'
        },
        status.HTTP_404_NOT_FOUND: {
            NotFound: 'RESOURCE_NOT_FOUND',
            Http404: 'RESOURCE_NOT_FOUND',
            'default': 'NOT_FOUND'
        },
        status.HTTP_405_METHOD_NOT_ALLOWED: {
            MethodNotAllowed: 'METHOD_NOT_ALLOWED',
            'default': 'METHOD_NOT_ALLOWED'
        },
        status.HTTP_409_CONFLICT: {
            'default': 'RESOURCE_CONFLICT'
        },
        status.HTTP_429_TOO_MANY_REQUESTS: {
            Throttled: 'RATE_LIMIT_EXCEEDED',
            'default': 'RATE_LIMIT_EXCEEDED'
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            'default': 'INTERNAL_SERVER_ERROR'
        },
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            'default': 'SERVICE_UNAVAILABLE'
        },
    }
    
    exc_type = type(exc)
    mapping = error_code_mapping.get(status_code, {})
    return mapping.get(exc_type, mapping.get('default', 'UNKNOWN_ERROR'))


def format_error_details(data):
    """
    Format DRF error details into a consistent structure.
    """
    if isinstance(data, dict):
        # DRF validation errors are typically dicts with field names as keys
        return {k: v if isinstance(v, list) else [str(v)] for k, v in data.items()}
    elif isinstance(data, list):
        # Non-field errors
        return {'non_field_errors': [str(item) for item in data]}
    else:
        return {'non_field_errors': [str(data)]}


def custom_exception_handler(exc, context):
    """
    Custom exception handler to provide consistent error responses with proper schemas.
    """
    # Generate request ID for tracking
    request_id = str(uuid.uuid4())[:8]
    
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)
    
    # Handle Django Http404
    if isinstance(exc, Http404):
        response = Response(
            status=status.HTTP_404_NOT_FOUND,
            data={
                'success': False,
                'error': {
                    'code': 'RESOURCE_NOT_FOUND',
                    'message': str(exc) or 'Resource not found',
                    'timestamp': datetime.utcnow().isoformat() + 'Z',
                    'request_id': request_id
                }
            }
        )
        return response

    if response is not None:
        # Get error code based on exception type and status
        error_code = get_error_code(exc, response.status_code)
        
        # Format error details
        error_details = format_error_details(response.data) if response.data else {}
        
        # Build consistent error response
        error_response = {
            'success': False,
            'error': {
                'code': error_code,
                'message': str(exc) if hasattr(exc, '__str__') else 'An error occurred',
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'request_id': request_id
            }
        }
        
        # Add details if available
        if error_details:
            error_response['error']['details'] = error_details
        
        # Special handling for specific error types
        if isinstance(exc, AuthenticationFailed):
            error_response['error']['message'] = 'Invalid authentication credentials'
        elif isinstance(exc, NotAuthenticated):
            error_response['error']['message'] = 'Authentication credentials were not provided'
        elif isinstance(exc, PermissionDenied):
            error_response['error']['message'] = 'You do not have permission to perform this action'
        elif isinstance(exc, Throttled):
            error_response['error']['message'] = 'Request was throttled'
            if hasattr(exc, 'wait'):
                error_response['error']['details'] = {
                    'retry_after': exc.wait,
                    'limit': getattr(exc, 'scope', 'unknown')
                }
        
        response.data = error_response
    
    # Handle unhandled exceptions (500 errors)
    elif response is None:
        # Log the exception in production (you can add logging here)
        error_response = {
            'success': False,
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'An internal server error occurred',
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'request_id': request_id
            }
        }
        
        # In development, include the actual error message
        from django.conf import settings
        if settings.DEBUG:
            error_response['error']['message'] = str(exc)
            error_response['error']['details'] = {
                'exception_type': type(exc).__name__,
                'traceback': str(exc)
            }
        
        response = Response(
            data=error_response,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return response


class APIException(Exception):
    """Base API exception."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = 'An error occurred'

    def __init__(self, message=None, status_code=None):
        self.message = message or self.default_message
        if status_code:
            self.status_code = status_code


class ValidationError(APIException):
    """Validation error exception."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = 'Validation error'


class NotFoundError(APIException):
    """Resource not found exception."""
    status_code = status.HTTP_404_NOT_FOUND
    default_message = 'Resource not found'


class PermissionDeniedError(APIException):
    """Permission denied exception."""
    status_code = status.HTTP_403_FORBIDDEN
    default_message = 'Permission denied'


class MLServiceError(APIException):
    """ML service error exception."""
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_message = 'ML service temporarily unavailable'


