from django.shortcuts import render

# 제네릭 뷰 (Generic Views)
"""
TemplateView : 단순히 템플릿을 렌더링하기 위한 클래스형 뷰로 GET 요청을 처리하고 template_name에 지정한 템플릿을 반환
 - 단순 페이지 렌더링 (ex: 안내 페이지, 정적 페이지, 결과 표시 페이지)
 - context에 몇 가지 값만 넘기면 되는 경우에 사용
 
✅ 왜 오버라이드 하나요?
기본 TemplateView는 템플릿에 아무 context도 안 넣어줌
직접 추가하지 않으면 템플릿에서 사용할 값이 없음
예: 페이지 제목, 리스트 데이터, 사용자 정보 등 주입하려는 경우

"""
from django.views.generic import TemplateView

class PageViewExample(TemplateView): # TemplateView를 상속 받아서 클래스형 뷰로 등록
    template_name = "path/template.html" # 렌더링할 템플릿 파일 경로를 지정, Django는 TEMPLATES['DIRS'] 또는 app_name/templates/ 경로에서 이 파일을 찾음

    def get_context_data(self, **kwargs): # 템플릿에 넘겨줄 context 딕셔너리를 구성, Django의 클래스형 뷰는 내부적으로 get_context_data()를 호출해 템플릿에 넘길 데이터를 구성함
        context = super().get_context_data(**kwargs) # 부모 클래스에서 제공하는 기본 context 값들(예: view, request, kwargs)을 유지
        context["변수명"] = '값' # 템플릿에서 사용할 추가 변수를 여기에 넣는 것
        return context


"""
👉 폼 처리 흐름 정의: 화면에 보여주고, 제출하고, 저장하고, 성공하면 어디로 갈지 등
FormView : 폼을 화면에서 보여주고 처리하는 전체 로직을 자동화한 뷰 클래스
"""
from django.views.generic import FormView
from .forms import LoginForm

# views.py
class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = "/dashboard/"

    def form_valid(self, form):
        user_id = form.cleaned_data['user_id']
        password = form.cleaned_data['password']
        # 로그인 처리 로직
        return super().form_valid(form)


"""
RedirectView : Django에서 URL 리다이렉트를 간편하게 처리해주는 클래스형 뷰
 - 정적 또는 동적으로 다른 URL로 이동만 시키는 용도
 
 > 다른 URL로 리디렉션(이동) 시킬 때 사용하는 클래스형 뷰
 > GET 요청을 받아서, 설정된 경로로 302 or 301 redirect
 > 파라미터, 쿼리스트링 등을 활용하여 동적 리다이렉트 가능
"""

"""커스터마이징된 RedirectView"""
from django.views.generic.base import RedirectView
from django.urls import reverse

class UciErrorRedirectView(RedirectView):
    permanent = False  # 302 리다이렉트
    query_string = True  # 기존 쿼리스트링 유지 가능 (예: ?page=2)

    def get_redirect_url(self, *args, **kwargs):
        # 예: 특정 조건에 따라 URL 결정
        uci_code = self.request.GET.get("uci")
        if uci_code:
            # 쿼리 파라미터를 붙여 리다이렉트
            return reverse("error_detail", kwargs={"uci": uci_code})
        return reverse("error_list")

