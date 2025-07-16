
"""
👉 폼 구조 정의: 어떤 입력값을 받을지, 어떻게 검증할지
Django Form : 사용자 입력을 처리하는 도구
- 일반 Form : forms.form > DB 모델과 무관한 입력 처리
- 모델 Form : forms.ModelForm > DB 모델과 자동으로 연동되는 폼 생성 (입출력 자동 처리)
"""


"""
일반 Form
 > 모델과 관계없이 순수한 폼 필드 수동 정의
 > 검증 로직 (clean()등)을 직접 구현 해야함
 > 로그인, 검색 폼 등 단순 입력 처리에 적합
"""
from django import forms

class LoginForm(forms.Form):
    user_id = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "관리자 ID",
                "class": "form-control",
                "id":"user_id"
    }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "비밀번호",
                "class": "form-control",
            }
        )
    )


    def clean(self):
        cleaned_data = super().clean()
        user_id = cleaned_data.get("user_id")
        password = cleaned_data.get("password")
        encrypted_password = EncryptUtil.md5_encrypt(password)

        try:
            user = Manager.objects.get(user_id=user_id)
            if not user.check_password(encrypted_password):
                self.add_error("password", "비밀번호가 틀렸습니다.")
        except Manager.DoesNotExist:
            self.add_error("user_id", "해당 사용자를 찾을 수 없습니다.")

        return cleaned_data

"""
모델 기반 Form
 > 특정 모델의 필드를 기반으로 자동 생성
 > DB 저장까지 자동 처리 가능 (form.save())
 > CRUD 화면 구현 시 매우 유용
"""
class EsGroupForm(forms.ModelForm):
    class Meta:
        model = U201EsProcess
        fields = ("status", "use_yn",)
        widgets = {
            "status": forms.Select(attrs={"class": "form-control, select2"}),
            "use_yn": forms.Select(attrs={"class": "form-control, select2"}),
        }
