"""
Common serializers for error responses and shared schemas.
"""
from rest_framework import serializers
from drf_spectacular.utils import inline_serializer


# Error Response Serializers for OpenAPI Schema
ErrorDetailSerializer = inline_serializer(
    name='ErrorDetail',
    fields={
        'code': serializers.CharField(help_text='Error code (e.g., VALIDATION_ERROR, AUTH_INVALID_TOKEN)'),
        'message': serializers.CharField(help_text='Human-readable error message'),
        'details': serializers.DictField(
            child=serializers.ListField(child=serializers.CharField()),
            required=False,
            help_text='Field-specific validation errors'
        ),
        'timestamp': serializers.DateTimeField(help_text='Error timestamp'),
        'request_id': serializers.CharField(required=False, help_text='Request ID for tracking')
    }
)

ErrorResponseSerializer = inline_serializer(
    name='ErrorResponse',
    fields={
        'success': serializers.BooleanField(default=False),
        'error': ErrorDetailSerializer
    }
)

# Common error response schemas for different status codes
ValidationErrorResponse = inline_serializer(
    name='ValidationErrorResponse',
    fields={
        'success': serializers.BooleanField(default=False),
        'error': inline_serializer(
            name='ValidationErrorDetail',
            fields={
                'code': serializers.CharField(default='VALIDATION_ERROR'),
                'message': serializers.CharField(),
                'details': serializers.DictField(
                    child=serializers.ListField(child=serializers.CharField())
                ),
                'timestamp': serializers.DateTimeField(),
            }
        )
    }
)

UnauthorizedErrorResponse = inline_serializer(
    name='UnauthorizedErrorResponse',
    fields={
        'success': serializers.BooleanField(default=False),
        'error': inline_serializer(
            name='UnauthorizedErrorDetail',
            fields={
                'code': serializers.CharField(default='AUTH_INVALID_TOKEN'),
                'message': serializers.CharField(),
                'timestamp': serializers.DateTimeField(),
            }
        )
    }
)

NotFoundErrorResponse = inline_serializer(
    name='NotFoundErrorResponse',
    fields={
        'success': serializers.BooleanField(default=False),
        'error': inline_serializer(
            name='NotFoundErrorDetail',
            fields={
                'code': serializers.CharField(default='RESOURCE_NOT_FOUND'),
                'message': serializers.CharField(),
                'timestamp': serializers.DateTimeField(),
            }
        )
    }
)

ForbiddenErrorResponse = inline_serializer(
    name='ForbiddenErrorResponse',
    fields={
        'success': serializers.BooleanField(default=False),
        'error': inline_serializer(
            name='ForbiddenErrorDetail',
            fields={
                'code': serializers.CharField(default='PERMISSION_DENIED'),
                'message': serializers.CharField(),
                'timestamp': serializers.DateTimeField(),
            }
        )
    }
)

ConflictErrorResponse = inline_serializer(
    name='ConflictErrorResponse',
    fields={
        'success': serializers.BooleanField(default=False),
        'error': inline_serializer(
            name='ConflictErrorDetail',
            fields={
                'code': serializers.CharField(default='RESOURCE_CONFLICT'),
                'message': serializers.CharField(),
                'timestamp': serializers.DateTimeField(),
            }
        )
    }
)

ServerErrorResponse = inline_serializer(
    name='ServerErrorResponse',
    fields={
        'success': serializers.BooleanField(default=False),
        'error': inline_serializer(
            name='ServerErrorDetail',
            fields={
                'code': serializers.CharField(default='INTERNAL_SERVER_ERROR'),
                'message': serializers.CharField(),
                'timestamp': serializers.DateTimeField(),
            }
        )
    }
)

