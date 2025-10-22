"""Custom exceptions for the application"""


class AppException(Exception):
    """Base exception for application errors"""
    pass


class ResourceNotFoundException(AppException):
    """Raised when a requested resource is not found"""
    pass


class DuplicateResourceException(AppException):
    """Raised when attempting to create a duplicate resource"""
    pass


class ValidationException(AppException):
    """Raised when validation fails"""
    pass
