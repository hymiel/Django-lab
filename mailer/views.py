"""
Django에서 내장 SMTP를 통한 메일 보내기
 * SMTP(Simple Mail Transfer Protocol) : 간이 전자 우편 전송 프로토콜(Simple Mail Transfer Protocol, SMTP)은 인터넷에서 이메일을 보내기 위해 이용되는 프로토콜
   - TCP Port No : 25
 * 상대 서버 지시를 위한 DNS의 MX 레코드가 사용되며, 메일 서버 간 송수신과 메일 클ㄹ라이언트에서 메일 서버로 메일을 보낼 때도 사용되는 경우가 있음
 * 텍스트 기반의 프로토콜로서 요구/응답 메시지뿐 아니라 모든 문자가 7bit ASCII로 되어있어야 한다고 규정되어 있기 때문에
    문자 표현에 8비트 이상의 코드를 사용하는 언어나 첨부파일과 자주 사용되는 각종 바이너리는 마임(MIME)이라고 불리는 방식으로 7비트로 변환되어 전달
 * 메시지를 생성하는 방법을 규정하지 않고 메시지 생성을 위하여 로컬 편집이나 단순한 전자 우편 응용이 사용.
   메시지가 생성되면 호출된 SMTP가 메시지를 받고 TCP를 이용하여 다른 호스트의 SMTP에게 전달

Gmail SMTP 서버를 이용해서 메일을 전송ㅎ 할 경우 Google Gmail Account 보안수준이 낮은 앱 > 허용
"""
from django.core.mail import EmailMessage
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from mailer.serializers import EmailSerializer


# Create your views here.

class SMTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # smtp사용해서 메일보내는 코드
            subject = "["+serializer.data['name']+"]의 문의" # 메일 제목
            to = ["@gmail.com"] # 문의 내용을 보낼 메일 주소, 리스트 형식
            message = serializer.data['comment'] # 메일 내용
            EmailMessage(subject=subject, body=message, to=to).send() # 메일 보내기
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)