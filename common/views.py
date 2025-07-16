"""
함수 기반 뷰 (Function-Based Views)
 - 정의: 순수 Python 함수로 요청(Request) → 응답(Response) 로직을 구현
 - 가독성이 좋고 직접적인 제어가 가능, 작은 기능이나 간단한 화면 처리에 적합한 로직
 - 반복 로직(인증/공통 처리 등)이 많아지면 중복이 늘어 날 수 있는 단점이 존재
"""
from django.shortcuts import render

def custom_404_view(request, exception):
    """
    handler404에 등록해서, DEBUG=False 환경에서
    404.html을 status=404로 반환
    """
    return render(request, 'includes/404.html', status=404)




def get_client_ip(self, request) -> str:
    """클라이언트 IP 주소 추출 함수"""
    # 프록시/로드밸런서가 설정한 원본 IP 주소를 가져옴
    # ex) '203.0.113.5, 70.41.3.18, 150.172.238.178'
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        # 가장 앞에 있는 IP가 실제 클라이언트 IP (프록시 체인 첫 번째)
        ip = x_forwarded_for.split(',')[0].strip() # IP 주소 양쪽 공백 제거 (안전 처리)
    else:
        # 프록시 정보가 없을 경우 기본 REMOTE_ADDR 사용 (직접 접속)
        ip = request.META.get('REMOTE_ADDR')

    return ip
