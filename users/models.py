from django.db import models

from groups.models import Group


# Create your models here.


class User(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=100)
    user_password = models.CharField(max_length=100)

    """GROUP-USER RELATIONAL"""
    group = models.ForeignKey(  # Group 모델을 참조함 (다대일 관계)
        Group, #
        related_name='users', # group_instance.users.all()로 해당 그룹의 유저 목록 조회 가능
        on_delete=models.CASCADE, # 그룹이 삭제되면, 연결된 유저들도 자동 삭제됨
        db_column='group_code' # 실제 DB의 외래키 컬럼명을 명시 (groups.group_code를 참조함)
    )


    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return self.user_id

    @property
    def is_anonymous(self):
        """
        이 객체가 **익명 사용자(로그인 안 한 유저)**인지 여부 반환
        AnonymousUser 클래스에서는 True
        여기에선	False → 즉, 로그인된 사용자처럼 동작
        """
        return False
    @property
    def is_authenticated(self):
        """
        Django 내부에서 이 객체가 인증된 사용자인지 검사할 때 사용
        request.user.is_authenticated 로 권한 체크할 때
        여기에선	True → 인증된 유저로 간주됨
        """
        return True
    @property
    def is_active(self):
        """
        이 계정이 비활성화된 계정인지 아닌지 나타냄
        Django 로그인 시스템이 로그인 허용 여부를 판단할 때
        여기에선	True → 활성 사용자로 간주됨
        """
        return True

"""
@property : 모델 필드가 아닌, 계산된 값이나 조합된 값을 속성처럼 사용하도록 커스터마이징

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"
        
>> user = User(first_name='현경', last_name='이')
>> print(user.full_name)  # 출력: 이 현경
"""

"""
__init__ : 일반적으로 Django Model에서 생성자 재정의는 다소 특수한 상황에서만 필요
 👉🏻 Django ORM은 모델 인스턴스를 생성/조회할 때 자동으로 초기화해주기 때문에 오버라이드 권장하지 않음
 👉🏻 외부 값을 추가적으로 저장하거나 로깅할 목적으로 쓸 수 있음
 
class Group(models.Model):
    group_code = models.CharField(max_length=10, primary_key=True)
    group_name = models.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        self.extra_info = kwargs.pop('extra_info', None)  # 커스텀 속성
        super().__init__(*args, **kwargs)
>> g = Group(group_code='G001', group_name='관리자', extra_info='외부전달값')
>> print(g.extra_info)  # '외부전달값'

"""

"""
save() : Override
 👉🏻 데이터를 저장하기 전에 가공하거나 검증이 필요할 때 사용
    예) 음수 가격 방지, 필드 자동 설정, 로그 남기기 등
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.price < 0:
            raise ValueError("가격은 0 이상이어야 합니다.")
        super().save(*args, **kwargs)  # 원래의 save() 호출
"""

"""
@property + save() 조합
예제: 세금 포함 가격 보여주기, 저장 시 세금 제외

@property는 계산된 값이나 표시용 값이고,
save()는 저장 시 값 가공/검사를 처리하므로,
두 기능을 같이 쓰면 "보여주는 값은 동적으로", "저장되는 값은 안전하게" 구현 가능

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 순수 가격 (세금 제외)

    @property
    def price_with_tax(self):
        return self.price * Decimal('1.1')  # 10% 세금 포함된 가격

    def save(self, *args, **kwargs):
        # 저장 전에 price가 음수인지 검사
        if self.price < 0:
            raise ValueError("가격은 음수가 될 수 없습니다.")
        super().save(*args, **kwargs)
        
>> p = Product(name="이어폰", price=10000)
>> print(p.price_with_tax)  # 11000.0 (계산된 값)
>> p.save()  # DB에는 10000만 저장
"""