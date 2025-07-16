# 토큰 발급/디코드 유틸

from django.utils import timezone
import jwt

from core import settings


class JWTUtil:
    @staticmethod
    def create_access_token(data: dict) -> str:
        """
        액세스 토큰 생성
            data : user_id 등 토큰에 필요한 모든 클레임을 dict 형식으로 전달
        """

        now = timezone.now()
        payload = {
            **data,  # 외부에서 넘겨준 클레임 모두 포함
            'token_type' : 'access',   # 토큰 종류 표시
            'iat': int(now.timestamp()), # 토큰 발급 시간
            'exp': int((now + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']).timestamp()),  # 만료 시각
        }

        token = jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.SIMPLE_JWT['ALGORITHM'],
        )

        # bytes -> str
        if isinstance(token, bytes):
            token = token.decode('utf-8')

        return token

    @staticmethod
    def create_refresh_token(data: dict) -> str:
        """
        리프레시 토큰 생성
            data: 액세스 토큰 때와 마찬가지로, 추가 클레임을 dict으로 전달
        """

        now = timezone.now()
        payload = {
            **data,
            'token_type' : 'refresh',
            'iat': int(now.timestamp()),
            'exp': int((now + settings.SIMPLE_JWT['JWT_REFRESH_TOKEN_LIFETIME']).timestamp()),
        }

        token = jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.SIMPLE_JWT['ALGORITHM'],
        )

        if isinstance(token, bytes):
            token = token.decode('utf-8')

        return token


    @staticmethod
    def decode_token(token: str) -> dict:
        """
        토큰 디코드
            반환값 : 토큰에 담긴 모든 클레임 > dict 로 반환
            만료 or 시그니처 불일치 할 경우 예외처리
        """
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.SIMPLE_JWT['ALGORITHM']],
            options={'require': ['exp', 'iat', 'token_type']}
        )
