"""Application constants."""

# File size constants (in bytes)
KB = 1024
MB = 1024 * KB
GB = 1024 * MB

MAX_IMAGE_SIZE = 10 * MB
MAX_VIDEO_SIZE = 100 * MB
MAX_PDF_SIZE = 50 * MB

# Image formats
SUPPORTED_IMAGE_FORMATS = ('PNG', 'JPG', 'JPEG', 'WEBP', 'BMP', 'TIFF', 'GIF')
SUPPORTED_DOCUMENT_FORMATS = ('PDF',)
SUPPORTED_VIDEO_FORMATS = ('MP4', 'AVI', 'MOV', 'MKV')

# Color space modes
RGB_COLOR_SPACE = 'RGB'
RGBA_COLOR_SPACE = 'RGBA'

# QR Code settings
QR_DEFAULT_SIZE = 10
QR_DEFAULT_BORDER = 4
QR_ERROR_CORRECTION_LEVELS = {
    'L': 1,
    'M': 0,
    'Q': 3,
    'H': 2,
}

# Default compression quality
DEFAULT_COMPRESSION_QUALITY = 85
MIN_COMPRESSION_QUALITY = 1
MAX_COMPRESSION_QUALITY = 100
