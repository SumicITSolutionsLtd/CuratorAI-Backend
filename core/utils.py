"""
Utility functions for CuratorAI.
"""
import hashlib
import uuid
from typing import Optional
from django.core.files.uploadedfile import UploadedFile
from PIL import Image
from io import BytesIO


def generate_unique_filename(original_filename: str, prefix: str = '') -> str:
    """
    Generate a unique filename using UUID.
    """
    ext = original_filename.split('.')[-1] if '.' in original_filename else ''
    unique_id = uuid.uuid4().hex
    return f"{prefix}{unique_id}.{ext}" if ext else f"{prefix}{unique_id}"


def validate_image_file(file: UploadedFile, max_size: int = 10 * 1024 * 1024) -> tuple[bool, Optional[str]]:
    """
    Validate uploaded image file.
    Returns (is_valid, error_message)
    """
    # Check file size
    if file.size > max_size:
        return False, f"File size exceeds maximum allowed size of {max_size / (1024 * 1024)}MB"
    
    # Check file type
    allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
    if file.content_type not in allowed_types:
        return False, f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
    
    # Validate image can be opened
    try:
        img = Image.open(file)
        img.verify()
        return True, None
    except Exception as e:
        return False, f"Invalid image file: {str(e)}"


def compress_image(image_file: UploadedFile, quality: int = 85, max_width: int = 1920) -> BytesIO:
    """
    Compress and resize image.
    """
    img = Image.open(image_file)
    
    # Convert RGBA to RGB if necessary
    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = background
    
    # Resize if too large
    if img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
    
    # Save to BytesIO
    output = BytesIO()
    img.save(output, format='JPEG', quality=quality, optimize=True)
    output.seek(0)
    return output


def calculate_file_hash(file: UploadedFile) -> str:
    """
    Calculate SHA256 hash of a file for duplicate detection.
    """
    file.seek(0)
    file_hash = hashlib.sha256()
    for chunk in file.chunks():
        file_hash.update(chunk)
    file.seek(0)
    return file_hash.hexdigest()


def success_response(data=None, message='Success', status_code=200):
    """
    Generate standardized success response.
    """
    response = {
        'success': True,
        'message': message,
    }
    if data is not None:
        response['data'] = data
    return response


def error_response(message='Error', errors=None, status_code=400):
    """
    Generate standardized error response.
    """
    response = {
        'success': False,
        'message': message,
    }
    if errors:
        response['errors'] = errors
    return response

