from django.views.generic.base import RedirectView
from django.urls import path

"""
기본 예시 (정적 리다이렉트)

/go-home/으로 요청하면 → /home/으로 리다이렉트
기본적으로 302 (Temporary Redirect) 응답을 보냄
"""
urlpatterns = [
    path('go-home/', RedirectView.as_view(url='/home/')),
]
from django.urls import path
from .views import UciErrorRedirectView

urlpatterns = [
    path("redirect-error/", UciErrorRedirectView.as_view(), name="uci_error_redirect"),
    path("errors/", ErrorListView.as_view(), name="error_list"),
    path("errors/<str:uci>/", ErrorDetailView.as_view(), name="error_detail"),
]

"""
고정 URL + 영구 리다이렉트 (permanent=True)

permanent=True이면 HTTP 301 (Moved Permanently) 응답
검색엔진이나 브라우저에 "영구 이전됨"을 알림
"""
path('old-page/', RedirectView.as_view(url='/new-page/', permanent=True)),

"""
정적 파일, 외부 URL로 리디렉트도 가능 
➡ 외부 URL도 리다이렉트 대상 가능
"""
path('docs/', RedirectView.as_view(url='https://docs.djangoproject.com/')),

"""
동적 URL 리다이렉트 (패턴 기반)
"""
path('go/<slug:target>/', RedirectView.as_view(pattern_name='destination')),
path('destination/<slug:target>/', some_view, name='destination')

