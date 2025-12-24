"""Validation utilities for image processing."""

import re
from django.core.exceptions import ValidationError


def validate_email(email):
    """Validate email address format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError('Invalid email format')
    return email


def validate_image_dimensions(image, min_width=1, min_height=1, max_width=10000, max_height=10000):
    """
    Validate image dimensions.
    
    Args:
        image: PIL Image object
        min_width, min_height: Minimum dimensions
        max_width, max_height: Maximum dimensions
    
    Raises:
        ValidationError: If dimensions are invalid
    """
    width, height = image.size
    
    if width < min_width or height < min_height:
        raise ValidationError(f'Image too small. Minimum: {min_width}x{min_height}')
    
    if width > max_width or height > max_height:
        raise ValidationError(f'Image too large. Maximum: {max_width}x{max_height}')


def validate_rgb_color(color):
    """
    Validate RGB color format (tuple or hex).
    
    Args:
        color: RGB tuple (r, g, b) or hex string
    
    Returns:
        Tuple (r, g, b)
    
    Raises:
        ValidationError: If color format is invalid
    """
    if isinstance(color, tuple) and len(color) == 3:
        if all(0 <= c <= 255 for c in color):
            return color
    
    if isinstance(color, str) and color.startswith('#'):
        try:
            hex_color = color.lstrip('#')
            if len(hex_color) == 6:
                r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                return (r, g, b)
        except ValueError:
            pass
    
    raise ValidationError('Invalid color format. Use RGB tuple or hex string')


def validate_positive_integer(value, name='value'):
    """Validate that value is a positive integer."""
    try:
        int_val = int(value)
        if int_val <= 0:
            raise ValidationError(f'{name} must be positive')
        return int_val
    except (ValueError, TypeError):
        raise ValidationError(f'{name} must be a valid integer')
