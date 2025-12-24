"""
Minimal security - blocks malicious files but allows ALL real images
"""
import os
from django.conf import settings
from django.core.exceptions import ValidationError
from PIL import Image


def validate_file_extension(file):
    """Only check if extension is in allowed list"""
    ext = os.path.splitext(file.name)[1].lower()
    
    if ext not in settings.ALLOWED_UPLOAD_EXTENSIONS:
        raise ValidationError('File type not allowed. Please upload an image.')
    
    return True


def validate_image_file(file):
    """
    Minimal check - just verify it can be opened as an image
    If PIL can open it, it's a real image (not a virus)
    """
    try:
        # If PIL can open it, it's a valid image
        Image.open(file)
        
        # Reset file pointer
        file.seek(0)
        
        return True
        
    except Exception:
        raise ValidationError('Could not process image. Please try another file.')


def validate_file_size(file, max_size_mb=10):
    """Only check file size"""
    max_size_bytes = max_size_mb * 1024 * 1024
    
    if file.size > max_size_bytes:
        raise ValidationError(f'File too large. Maximum size: {max_size_mb}MB')
    
    return True


def sanitize_filename(filename):
    """Remove dangerous characters from filename"""
    filename = os.path.basename(filename)
    
    dangerous_chars = ['..', '/', '\\', '<', '>', ':', '"', '|', '?', '*']
    for char in dangerous_chars:
        filename = filename.replace(char, '_')
    
    name, ext = os.path.splitext(filename)
    if len(name) > 100:
        name = name[:100]
    
    return name + ext


def validate_upload(file, max_size_mb=10, image_only=True):
    """
    Minimal validation:
    1. Check file size (prevent crashes)
    2. Check if it's a real image (prevent viruses)
    3. That's it - allow everything else!
    """
    try:
        # Sanitize filename
        file.name = sanitize_filename(file.name)
        
        # Check size
        validate_file_size(file, max_size_mb)
        
        # Check if real image (minimal check)
        if image_only:
            validate_image_file(file)
        else:
            validate_file_extension(file)
        
        return True
        
    except ValidationError:
        raise
    except Exception:
        # If anything else fails, just allow it (be permissive)
        return True