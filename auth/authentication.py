from asyncio import exceptions

import jwt
from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions
from core import settings
from django.utils.translation import gettext_lazy as _

# 활성 User 모델 가져오기 (커스텀 또는 기본 Django User)
User = get_user_model()

class JWTAuthentication(authentication.BaseAuthentication):
    """
    DRF 인증 백엔드(JWT)
    HTTP_AUTHORIZATION 헤더에서 'Bearer <token>' 스킴을 파싱하고,
    JWT payload를 디코드한 뒤 user_id로 사용자 조회하여 인증 처리
    """

    # Authorization 헤더 접두사, 예: 'Bearer'
    auth_header_prefix = settings.SIMPLE_JWT.get('AUTH_HEADER_TYPES', ('Bearer',))[0]
    # 토큰 서명 및 검증에 사용할 키 (기본으로 SECRET_KEY 사용)
    signing_key       = settings.SIMPLE_JWT.get('SIGNING_KEY', settings.SECRET_KEY)
    # 사용할 알고리즘 (예: 'HS256')
    algorithm         = settings.SIMPLE_JWT.get('ALGORITHM', 'HS256')
    # payload에서 반드시 포함되어야 하는 클레임 집합
    required_claims   = {'exp', 'iat', 'token_type', 'user_id'}

    def authenticate(self, request):
        # HTTP_AUTHORIZATION 헤더 가져오기
        header = request.META.get('HTTP_AUTHORIZATION', '')
        # 헤더가 지정된 접두사로 시작하지 않으면 인증 시도하지 않음
        if not header.startswith(self.auth_header_prefix):
            return None

        # 'Bearer <token>' 형태로 분리
        parts = header.split()
        # ['Bearer', '<token>'] 형태여야 함
        if len(parts) != 2:
            raise exceptions.AuthenticationFailed(
                _("Authorization 헤더 형식이 올바르지 않습니다.")
            )

        token = parts[1]  # 실제 JWT 문자열
        try:
            # JWT 디코딩: 서명 및 만료 검증, 필수 클레임 검사
            payload = jwt.decode(
                token,
                self.signing_key,
                algorithms=[self.algorithm],
                options={'require': list(self.required_claims)}
            )
        except jwt.ExpiredSignatureError:
            # 토큰 만료된 경우
            raise exceptions.AuthenticationFailed(_("액세스 토큰이 만료되었습니다."))
        except jwt.InvalidTokenError:
            # 토큰 유효하지 않은 경우
            raise exceptions.AuthenticationFailed(_("유효하지 않은 액세스 토큰입니다."))

        # 토큰 타입이 access여야 함
        if payload.get('token_type') != 'access':
            raise exceptions.AuthenticationFailed(_("토큰 타입이 올바르지 않습니다."))

        # payload에서 사용자 ID 추출
        user_id = payload.get('user_id')
        try:
            # DB에서 사용자 조회
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            # 사용자 없음
            raise exceptions.AuthenticationFailed(_("사용자를 찾을 수 없습니다."))

        # 비활성화된 사용자 차단
        if not user.is_active:
            raise exceptions.AuthenticationFailed(_("비활성 사용자입니다."))

        # 인증된 사용자와 credentials(None) 반환
        return (user, None)