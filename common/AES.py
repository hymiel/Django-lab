"""
AES-CBC 암호화/복호화 유틸

KEY : SHA-256 해시를 사용하여 임의 길이 문자열을 32Byte(256Bit) AES 키로 변환
IV : 암호문 앞에 랜덤 IV (16Byte) 저장 > 복호화 시 앞쪽 IV(16Byte) 자른 뒤 사용
패딩: PKCS#7(pad/unpad)
문자열 입출력: Base64 인코딩으로 텍스트 형태 입출력
"""
import base64
import hashlib
from typing import ClassVar
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

class AESUtil:
    """
    AES‑CBC 암호화/복호화 유틸리티

    - AES 블록 크기: 16바이트
    - 키: SHA‑256 해시로 32바이트(256비트) 생성
    - IV: 암호화 시마다 랜덤 생성, 암호문 앞에 붙여 저장
    """

    BLOCK_SIZE : ClassVar[int] = AES.block_size #16
    KEY_SIZE : ClassVar[int] = 32 #256Byte Key

    @staticmethod
    def _derive_key(secret : str) -> bytes:
        """
        임의 길이 문자열(secret) → 32바이트 AES 키 변환
        """
        return hashlib.sha256(secret.encode('utf-8')).digest()

    @classmethod
    def encrypt(cls, plaintext: str, secret: str) -> str:
        """
        AES‑CBC 암호화

        1. 키 = SHA‑256(secret)
        2. IV = get_random_bytes(16)
        3. ciphertext = AES.new(key, CBC, iv).encrypt(pad(plaintext))
        4. return base64(iv + ciphertext)
        """
        key_bytes = cls._derive_key(secret)
        iv        = get_random_bytes(cls.BLOCK_SIZE)
        cipher    = AES.new(key_bytes, AES.MODE_CBC, iv)
        padded    = pad(plaintext.encode('utf-8'), cls.BLOCK_SIZE)
        encrypted = cipher.encrypt(padded)
        # IV를 앞에 붙이고 Base64 인코딩
        return base64.b64encode(iv + encrypted).decode('utf-8')

    @classmethod
    def decrypt(cls, b64_ciphertext: str, secret: str) -> str:
        """
        AES‑CBC 복호화

        1. raw = base64.b64decode(b64_ciphertext)
        2. iv = raw[:16], ciphertext = raw[16:]
        3. plaintext = unpad(AES.new(key, CBC, iv).decrypt(ciphertext))
        """
        raw = base64.b64decode(b64_ciphertext)
        iv  = raw[:cls.BLOCK_SIZE]
        ct  = raw[cls.BLOCK_SIZE:]
        key_bytes = cls._derive_key(secret)
        cipher    = AES.new(key_bytes, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(ct)
        return unpad(decrypted, cls.BLOCK_SIZE).decode('utf-8')

    @staticmethod
    def md5_hash(data: str) -> str:
        """
        MD5 해시를 계산한 뒤 Base64 인코딩하여 반환
        """
        digest = hashlib.md5(data.encode('utf-8')).digest()
        return base64.b64encode(digest).decode('utf-8')
# ===================================================================================================
"""사용예시"""
from core.settings import AES_KEY  # .env에 저장된 문자열 키

# 암호화
cipher_text = AESUtil.encrypt("비밀 메시지", AES_KEY)

# 복호화
plain_text = AESUtil.decrypt(cipher_text, AES_KEY)

# MD5 해시
hash_text = AESUtil.md5_hash("임의 문자열")

# ===================================================================================================
"""
PHP 방식 호환 - 예시
AES 암복호화 / MD5 사용
"""
# import base64
# import hashlib
# from typing import Final
#
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad, unpad
#
# from core.settings import AES_KEY
#
# # AES_KEY는 settings.py에서 정의한 암호화 키 문자열
# key: Final = AES_KEY                # AES 키 (문자열)
# encoded_key: Final = key.encode('utf-8')  # 문자열 키를 바이트로 인코딩
#
# # 고정 IV (16바이트 0x00) - PHP 기본 방식과 호환 목적
# iv: Final = b'\x00' * 16
#
# class AESUtil:
#     @staticmethod
#     def decrypt(encrypted_str: str, request_key: str = None, request_iv: bytes = None) -> str:
#         """
#         AES-CBC 복호화 함수
#         :param encrypted_str: Base64로 인코딩된 암호문 문자열
#         :param request_key:  옵션 키 (없으면 settings.AES_KEY 사용)
#         :param request_iv:   옵션 IV (없으면 고정된 iv 사용)
#         :return: 복호화된 평문 문자열
#         """
#         # 1) 암호문을 Base64 디코딩하여 바이트 배열로 변환
#         encrypted_data = base64.b64decode(encrypted_str)
#         # 2) 키와 IV 선택: 요청으로 받은 값이 없으면 기본값 사용
#         cipher_key = encoded_key if request_key is None else request_key.encode('utf-8')
#         cipher_iv  = iv          if request_iv   is None else request_iv
#         # 3) AES-CBC 모드로 복호화 객체 생성
#         cipher = AES.new(cipher_key, AES.MODE_CBC, cipher_iv)
#         # 4) 복호화 실행
#         decrypted = cipher.decrypt(encrypted_data)
#         # 5) 길이가 0이면 빈 바이트 반환
#         if len(decrypted) == 0:
#             return decrypted
#         # 6) PKCS#7 패딩 제거 후 UTF-8 문자열로 디코딩
#         decrypted_text = unpad(decrypted, AES.block_size).decode('utf-8')
#         return decrypted_text
#
#     @staticmethod
#     def encrypt(text: str) -> str:
#         """
#         AES-CBC 암호화 함수
#         :param text: 평문 문자열
#         :return: Base64로 인코딩된 암호문 문자열
#         """
#         # 1) 평문을 바이트로 인코딩 후 PKCS#7 패딩 추가
#         padded_text = pad(text.encode('utf-8'), AES.block_size)
#         # 2) AES-CBC 암호화 객체 생성 (기본 키·IV 사용)
#         cipher = AES.new(encoded_key, AES.MODE_CBC, iv)
#         # 3) 암호화 실행
#         encrypted_bytes = cipher.encrypt(padded_text)
#         # 4) 암호문을 Base64 문자열로 인코딩하여 반환
#         encrypted_base64 = base64.b64encode(encrypted_bytes).decode('utf-8')
#         return encrypted_base64
#
#     @staticmethod
#     def md5_encrypt(data: str) -> str:
#         """
#         MD5 해시를 계산한 뒤 Base64 인코딩
#         :param data: 해시할 문자열
#         :return: Base64 인코딩된 MD5 해시 값
#         """
#         # 1) MD5 다이제스트(바이트) 계산
#         md5_hash = hashlib.md5(data.encode('utf-8')).digest()
#         # 2) Base64로 인코딩하여 반환
#         b64_encoded = base64.b64encode(md5_hash).decode('utf-8')
#         return b64_encoded
