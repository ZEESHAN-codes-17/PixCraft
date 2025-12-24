"""File handling utilities for image processing."""

import os
from django.core.exceptions import ValidationError
from PIL import Image


def validate_upload(file, max_size_mb=10, image_only=True):
    """
    Validate uploaded file size and type.
    
    Args:
        file: Django UploadedFile object
        max_size_mb: Maximum file size in MB
        image_only: If True, only accept image files
    
    Raises:
        ValidationError: If file is invalid
    """
    max_size = max_size_mb * 1024 * 1024
    
    if file.size > max_size:
        raise ValidationError(f'File size exceeds {max_size_mb}MB limit')
    
    if image_only:
        valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff'}
        file_ext = os.path.splitext(file.name)[1].lower()
        
        if file_ext not in valid_extensions:
            raise ValidationError(f'Invalid file type. Allowed: {", ".join(valid_extensions)}')
        
        try:
            img = Image.open(file)
            img.verify()
        except Exception:
            raise ValidationError('Invalid image file or corrupted image')


def sanitize_filename(filename):
    """
    Sanitize filename by removing potentially unsafe characters.
    
    Args:
        filename: Original filename
    
    Returns:
        Sanitized filename
    """
    import re
    
    # Remove path separators and other unsafe characters
    filename = os.path.basename(filename)
    filename = re.sub(r'[^\w\s.-]', '', filename)
    filename = re.sub(r'[\s]+', '_', filename)
    
    return filename or 'file'


def get_file_extension(filename):
    """Get file extension from filename."""
    return os.path.splitext(filename)[1].lower()


def generate_filename(original_filename, prefix='', suffix=''):
    """Generate a new filename with optional prefix and suffix."""
    name, ext = os.path.splitext(original_filename)
    return f"{prefix}{name}{suffix}{ext}"
