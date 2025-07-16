"""
URL configuration for DjangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from core import settings

#########################################
# Swagger 스키마 뷰 정의 : OpenAPI(Swagger) 스펙 문서를 생성해 주는 뷰 팩토리 함수
#########################################
"""
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication


schema_view = get_schema_view(
    openapi.Info( #openapi.Info: API 메타데이터를 담는 객체
        title="Django REST API",
        default_version='v1',
        description="API 문서입니다.",
        contact=openapi.Contact(email="support@example.com"),
    ),
    public=False,  # public=False이면 authentication_classes + permission_classes 모두 적용
    authentication_classes=(                    # ← 여기에 인증 클래스 지정
        SessionAuthentication,                  # Django 세션 쿠키 기반 인증
        BasicAuthentication,                    # HTTP Basic Auth
        JWTAuthentication,                      # JWT 토큰 인증
    ),
    permission_classes=(permissions.IsAuthenticated,),  # 인증된 사용자만 접근 허용
)
"""

urlpatterns = [
    path('admin/', admin.site.urls),

    """API URL"""
    # path('api/v1/groups', include("groups.api.urls")),
    """Swagger UI (인터랙티브 API 문서)"""
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    """ReDoc UI (다른 스타일의 API 문서)"""
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

#########################################
# 404 페이지 핸들러
#########################################

handler404 = 'common.views.custom_404_view'

#########################################
# 파일 제공
#########################################
from django.conf.urls.static import static

if settings.DEBUG:
   # STATIC 파일 제공
   urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)

   # MEDIA 파일 제공
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)