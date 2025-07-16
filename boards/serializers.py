"""
 serializers는 모델 객체 ↔ JSON 간 변환을 담당하며, API의 핵심 구성요소
 serializers.ModelSerializer (모델 기반 시리얼라이저) : 모델 연동 시 사용하며 CRUD 자동 처리
 serializers.Serializer	(모델 비연동) : 유효성 검사, 출력 자유도가 높음
"""

"""ModelSerializer"""
from rest_framework import serializers
from .models import Board

class BoardSerializer(serializers.ModelSerializer):
    summary = serializers.SerializerMethodField() #커스텀 필드 추가
    class Meta:
        model = Board # 연결할 모델
        fields = ['id', 'title', 'content', 'created_at'] # 출력/입력 대상 필드 목록 '__all__'로 모든 필드 입력이 가능하지만 유지보수상 직접 명시하는게 좋음
        read_only_fields = ['id', 'created_at'] # GET은 포함하지만 POST/PUT에서는 제외할 필드
        extra_kwargs = { # 개별 필드의 read_only, required, validators 설정
            'title': {'required': True, 'max_length': 100},
            'content': {'allow_blank': False}
        }

    # 커스텀 필드 추가
    def get_summary(self, obj):
        return obj.content[:30] + "..."


"""Serializer"""
class LoginSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=30)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(user_id=data['user_id'], password=data['password'])
        if not user:
            raise serializers.ValidationError("인증 실패")
        return data

"""Serializer - 관계 필드 기본"""
class BoardSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    # 또는 PrimaryKeyRelatedField(), SlugRelatedField()

    class Meta:
        model = Board
        fields = ['id', 'title', 'author']

"""Serializer - Nested serializer => 읽기 전용으로만 Nested 사용. 쓰기까지 하려면 create()/update() 오버라이드 필요"""
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']

class BoardSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Board
        fields = ['id', 'title', 'author']

"""create()/update() 오버라이드 (직접 저장 제어) => 복잡한 저장 처리 가능"""
class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['title', 'content']

    def create(self, validated_data):
        return Board.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
