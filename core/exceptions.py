"""
Custom exception handlers for CuratorAI API.
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler to provide consistent error responses.
    """
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {
            'success': False,
            'error': {
                'message': str(exc),
                'details': response.data
            }
        }
        response.data = custom_response_data

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

