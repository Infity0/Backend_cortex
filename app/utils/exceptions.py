from fastapi import HTTPException, status


class AppException(HTTPException):
    """Base application exception"""
    pass


class ValidationException(AppException):
    """Validation error"""
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


class NotFoundException(AppException):
    """Resource not found"""
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class UnauthorizedException(AppException):
    """Unauthorized access"""
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class ForbiddenException(AppException):
    """Forbidden access"""
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class ConflictException(AppException):
    """Resource conflict"""
    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class InsufficientTokensException(AppException):
    """Insufficient tokens"""
    def __init__(self, detail: str = "Insufficient tokens"):
        super().__init__(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=detail)
