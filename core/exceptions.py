"""Custom exceptions for the project."""


class ImageProcessingError(Exception):
    """Raised when image processing fails."""
    pass


class ValidationError(Exception):
    """Raised when validation fails."""
    pass


class FileUploadError(Exception):
    """Raised when file upload fails."""
    pass


class LinkExpiredError(Exception):
    """Raised when an image link has expired."""
    pass
