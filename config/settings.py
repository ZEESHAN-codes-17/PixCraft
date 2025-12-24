"""
Consolidated settings configuration.
This module can be extended to include environment-specific settings.
"""

from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY SETTINGS
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

# FILE UPLOAD SETTINGS
MAX_UPLOAD_SIZE_MB = 10
DATA_UPLOAD_MAX_MEMORY_SIZE = MAX_UPLOAD_SIZE_MB * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = MAX_UPLOAD_SIZE_MB * 1024 * 1024

ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff']
ALLOWED_UPLOAD_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS + ['.pdf', '.mp4', '.avi', '.mov']

# IMAGE PROCESSING SETTINGS
IMAGE_PROCESSING = {
    'max_width': 10000,
    'max_height': 10000,
    'default_compression_quality': 85,
    'default_thumbnail_size': (200, 200),
}

# EMAIL CONFIGURATION
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

# RATE LIMITING SETTINGS
RATE_LIMIT_SETTINGS = {
    'image_to_pdf': '20/h',
    'format_converter': '30/h',
    'image_compressor': '30/h',
    'qr_generator': '40/h',
    'image_link_generator': '25/h',
}

# IMAGE LINK EXPIRY SETTINGS
IMAGE_LINK_EXPIRY_CHOICES = [
    ('1h', '1 Hour'),
    ('1d', '1 Day'),
    ('7d', '7 Days'),
    ('1m', '1 Month'),
]
