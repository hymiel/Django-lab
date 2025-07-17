"""
Django Basic Exception
1. Http404 : 존재하지 않는 객체 접근 시 404 page render
2. PermissionDenied : 권한 없음 403 page render
3. SuspiciousOperation : 보안 관련 오류 (예: CSRF, Host header 오류) 400 Bad Request
4. Exception : 일반 서버 에러 500 page render

"""

"""CustomAPIException : 기반 예외 클래스 만들기"""
# exceptions/base.py
from rest_framework.exceptions import APIException
from rest_framework import status

class CustomAPIException(APIException):
    def __init__(self, status_code=status.HTTP_400_BAD_REQUEST, reason="Bad Request", message="요청이 잘못되었습니다."):
        self.status_code = status_code
        self.detail = {
            "status": status_code,
            "reason": reason,
            "message": message,
            "data": None
        }


""" DRF 전체 예외를 이 포맷으로 맞추고 싶을 때"""
# exceptions/handler.py
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and isinstance(response.data, dict):
        return Response({
            "status": response.status_code,
            "reason": exc.__class__.__name__,
            "message": response.data.get('detail', '요청 처리 중 오류 발생'),
            "data": None
        }, status=response.status_code)

    return Response({
        "status": 500,
        "reason": "InternalServerError",
        "message": "서버 내부 오류가 발생했습니다.",
        "data": None
    }, status=500)
