"""
Django Middleware는 요청(request)과 응답(response) 사이에서 작동하는 후크(Hook) 시스템
즉, Django가 요청(Request)을 처리하기 전/후 또는 응답(Response)을 반환하기 전/후에 자동으로 개입할 수 있도록 만든 전역 처리 로직

 > 요청 인증 / 권한 검사
 > 로깅 / IP 추적
 > 예외 처리
 > CORS, GZip 압축
 > 사용자 맞춤 언어 설정
 > 응답 헤더 수정 등


📈 Request 처리 과정
클라이언트 → 요청(Request) 발생
Middleware.process_request() 호출
뷰(View) 실행
Middleware.process_view() (옵션)
뷰의 응답 반환
Middleware.process_response() 호출
응답 반환 → 클라이언트

🧩 실제 동작 구조 (ASGI/WSGI)
request ---> middleware1 ---> middleware2 ---> view ---> middleware2 ---> middleware
"""

"""IP 로깅 미들웨어: 모든 요청의 IP 주소를 출력하고, 응답에 버전 정보를 추가"""
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        # Django가 view를 호출하기 전 실행됨 (1회 초기화)
        self.get_response = get_response

    def __call__(self, request):
        # 요청 전 처리: 클라이언트 IP 출력
        ip = request.META.get("REMOTE_ADDR")
        print(f"[Request IP]: {ip}")

        # view 또는 다음 미들웨어 호출
        response = self.get_response(request)

        # 응답 전 처리: 응답 헤더에 앱 버전 정보 추가
        response["X-App-Version"] = "1.0.0"
        return response

"""LoginRequiredMiddleware: 로그인하지 않은 사용자는 특정 URL을 제외하고 로그인 페이지로 리다이렉트"""
from django.shortcuts import redirect
from django.urls import resolve, reverse
from rest_framework.permissions import BasePermission  # (사용 안 하므로 제거 가능)

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        # 미들웨어 초기화 (1회)
        self.get_response = get_response

    def __call__(self, request):
        # 현재 요청된 URL 이름 추출
        current_url = resolve(request.path_info).url_name

        # 로그인 없이 접근 허용할 URL 목록
        login_exempt_urls = ['login', 'api', 'check_session_status']

        # 세션에서 로그인 여부 확인
        user_id = request.session.get("user_id")

        # 로그인이 안 되어 있고, 예외 URL이 아닐 경우 → 로그인 페이지로 리다이렉트
        if not user_id and current_url not in login_exempt_urls:
            return redirect(reverse("managers:login"))

        # 정상 요청 처리
        response = self.get_response(request)
        return response


"""Logging Middeleware"""
import logging
import json
from datetime import datetime

access_logger = logging.getLogger('access_logger')
error_logger = logging.getLogger('error_logger')

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_time = datetime.utcnow().isoformat()
        ip = self._get_client_ip(request)
        method = request.method
        path = request.get_full_path()

        try:
            response = self.get_response(request)
            # 정상 응답 로깅
            access_logger.info(json.dumps({
                "timestamp": request_time,
                "ip": ip,
                "method": method,
                "path": path,
                "status": response.status_code
            }))
            return response

        except Exception as e:
            # 에러 발생 시 error_logger에 기록
            error_logger.error(json.dumps({
                "timestamp": request_time,
                "ip": ip,
                "method": method,
                "path": path,
                "error": str(e)
            }), exc_info=True)
            raise  # 예외 다시 던짐

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')
