from django.db import models

from common.constants import GROUP_TYPE_CHOICES


# Create your models here.
"""
Django ORM Model 정의 모듈
"""

class Group(models.Model):
    """
    [Option]
    max_length : 최대 문자열 길이
    primary_key : (bool) PK 여부
    null : (bool)실제 데이터베이스에서 참조할 테이블 이름을 명시
    blank : (boll) form에서 빈값 허용 여부
    default : 기본값 지정
    choices : 선택지 제한 (튜플 리스트 사용 - constants.py)
    verbose_name : 관리자 페이지에서 표시 할 필드 이름
    help_text : 관리자 페이지 or form에서 도움말 텍스트 표시
    unique : 유일값 여부 (중복 불가)
    db_index : DB 인덱스 설정 여부
    editable : 장고 어드민에서 수정 가능 여부
    validators : 유효성 검사 함수 목록

    [Field]
    CharField : 고정 길이의 문자열
    TextField : 긴 텍스트 (게시판 글 내용 등)
    IntegerField : 정수 (BigIntegerField : 매우 큰 정수, PositiveIntegerField : 0 이상의 정수)
    FloatField : 실수 - 부동 소수점 (DecimalField : 고정 소수점 숫자 - 금액)
    DateField : 날짜 (YYYY-MM-DD)
    DateTimeField : 날짜(YYYY-MM-DD) + 시간
    TimeField : 시간(HH:MM:SS)
    EmailField : 이메일 주소
    URLField : URL 주소
    FileField : 파일 업로드 필드
    ImageField : 이미지 업로드 필드
    JSONField : JSON 데이터 저장 (PostgreSQL 등 지원)
    ForeignKey : 외래 키 (다대일 관계)
    OneToOneField : 일대일 관계
    ManyToManyField :다대다 관계
    """
    
    group_code = models.CharField(max_length=8, primary_key=True)
    group_name = models.CharField(max_length=250, null=False)
    group_type = models.CharField(max_length=250, choices=GROUP_TYPE_CHOICES ,null=True)


    class Meta:
        """
        managed : Django가 이 테이블에 대해 마이그레이션을 생성하거나 관리할 지 여부
        db_table : 실제 데이터베이스에서 참조할 테이블 이름을 명시
        unique_together : PK가 여러개 인 경우, DB에 명시하되, 해당 기능을 사용하여 PK 모두 명시
        """
        # managed = True
        managed = False
        db_table = 'groups'
        unique_together = ("", "", "")

    def __str__(self):
        """
        모델 인스턴스를 문자열로 표현할 때의 값을 정의하는 함수

        >> group = Group(group_code="G001", group_name="관리자 그룹")
        >> print(group)

        __str__ 메서드가 없다면: <Group object (G001)>
        __str__ 메서드가 있다면: G001 또는 원하는 출력값
        """
        return self.group_code
    
"""예시 조합"""
# from django.db import models
# import uuid
# 
# class Example(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     image = models.ImageField(upload_to='uploads/', null=True, blank=True)
#     unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
