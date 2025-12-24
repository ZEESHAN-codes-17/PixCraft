"""Core image processing service."""

import io
from PIL import Image
from django.core.exceptions import ValidationError


class ImageProcessor:
    """Service for image processing operations."""
    
    SUPPORTED_FORMATS = ['PNG', 'JPG', 'JPEG', 'WEBP', 'BMP', 'TIFF', 'GIF']
    
    @staticmethod
    def open_image(file):
        """
        Open image from file.
        
        Args:
            file: Django UploadedFile object
        
        Returns:
            PIL Image object
        """
        try:
            img = Image.open(file)
            img.load()
            return img
        except Exception as e:
            raise ValidationError(f'Failed to open image: {str(e)}')
    
    @staticmethod
    def resize_image(image, width, height, maintain_aspect=True):
        """
        Resize image to specified dimensions.
        
        Args:
            image: PIL Image object
            width: Target width
            height: Target height
            maintain_aspect: If True, maintain aspect ratio
        
        Returns:
            Resized PIL Image object
        """
        if maintain_aspect:
            image.thumbnail((width, height), Image.Resampling.LANCZOS)
        else:
            image = image.resize((width, height), Image.Resampling.LANCZOS)
        return image
    
    @staticmethod
    def convert_format(image, output_format):
        """
        Convert image to different format.
        
        Args:
            image: PIL Image object
            output_format: Target format (PNG, JPG, WEBP, etc.)
        
        Returns:
            Bytes object of converted image
        """
        output_format = output_format.upper()
        
        if output_format not in ImageProcessor.SUPPORTED_FORMATS:
            raise ValidationError(f'Unsupported format: {output_format}')
        
        if output_format == 'JPG':
            output_format = 'JPEG'
        
        if image.mode in ('RGBA', 'LA', 'P') and output_format == 'JPEG':
            image = image.convert('RGB')
        
        buffer = io.BytesIO()
        image.save(buffer, format=output_format, quality=95)
        buffer.seek(0)
        
        return buffer.getvalue()
    
    @staticmethod
    def compress_image(image, quality=85):
        """
        Compress image by reducing quality.
        
        Args:
            image: PIL Image object
            quality: Compression quality (1-100)
        
        Returns:
            Bytes object of compressed image
        """
        quality = max(1, min(100, int(quality)))
        
        output_format = image.format or 'JPEG'
        if output_format == 'PNG':
            image = image.convert('RGB')
            output_format = 'JPEG'
        
        buffer = io.BytesIO()
        image.save(buffer, format=output_format, quality=quality, optimize=True)
        buffer.seek(0)
        
        return buffer.getvalue()
    
    @staticmethod
    def rotate_image(image, angle):
        """
        Rotate image by specified angle.
        
        Args:
            image: PIL Image object
            angle: Rotation angle in degrees (negative = clockwise)
        
        Returns:
            Rotated PIL Image object
        """
        return image.rotate(-angle, expand=True)
    
    @staticmethod
    def convert_to_rgb(image):
        """Convert image to RGB mode."""
        if image.mode != 'RGB':
            image = image.convert('RGB')
        return image
    
    @staticmethod
    def save_to_buffer(image, format='PNG', quality=95):
        """
        Save image to bytes buffer.
        
        Args:
            image: PIL Image object
            format: Image format
            quality: Compression quality (if applicable)
        
        Returns:
            BytesIO buffer
        """
        buffer = io.BytesIO()
        image.save(buffer, format=format, quality=quality)
        buffer.seek(0)
        return buffer
