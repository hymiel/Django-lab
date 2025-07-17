

"""세부 커스텀 예외 정의"""
# exceptions/custom.py
from rest_framework import status

from common.exceptions import CustomAPIException


class DatabaseResultException(CustomAPIException):
    def __init__(self, message="DB 결과가 유효하지 않습니다."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            reason="Database Result Error",
            message=message
        )

class UnauthorizedAccessException(CustomAPIException):
    def __init__(self, message="인증되지 않은 접근입니다."):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            reason="Unauthorized Access",
            message=message
        )

class ResourceNotFoundException(CustomAPIException):
    def __init__(self, message="요청한 리소스를 찾을 수 없습니다."):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            reason="Resource Not Found",
            message=message
        )


class BadRequestException(CustomAPIException):
    def __init__(self, message="요청 파라미터가 잘못되었습니다."):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            reason="Bad Request",
            message=message
        )


class DuplicateResourceException(CustomAPIException):
    def __init__(self, message="이미 존재하는 리소스입니다."):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            reason="Duplicate Resource",
            message=message
        )


class ForbiddenAccessException(CustomAPIException):
    def __init__(self, message="이 작업에 대한 권한이 없습니다."):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            reason="Forbidden",
            message=message
        )


class ServiceUnavailableException(CustomAPIException):
    def __init__(self, message="현재 서비스 이용이 불가능합니다."):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            reason="Service Unavailable",
            message=message
        )