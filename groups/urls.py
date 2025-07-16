
"""
path() 기반 URL 설정
 - 일반적인 웹 페이지 URL을 구성
 - REST API를 수동으로 만드는 경우
 - VIEW나 URL 구조가 단순한 경우

DefaultRouter 기반 URL 설정 (Django Rest Framework ViewSet용)
 - REST API를 빠르게 구성할 때
 - ViewSet + 직관적인 CRUD 구조를 원할 때
 - Django Admin 수준의 코드량으로 API 만들고 싶을 때
"""


"""
path() 기반 URL 설정

path('URL 경로', 뷰 함수 또는 클래스(view:함수형 뷰(Function-based view) or as_view():클래스형 뷰(Class-based view)), URL이름 (name='')),

[예시]
from django.urls import path
urlpatterns = [
    path('tracks/<str:uci>/', SongDetailView.as_view(), name='track_details'),
]
"""

"""
DefaultRouter 기반 URL 설정
router.register("루트 경로:접두 URL", ViewSet 클래스(CRUD 처리), basename="URL name prefix")

[예시]
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register("", ViewSet, basename="metas")
urlpatterns = router.urls

"""