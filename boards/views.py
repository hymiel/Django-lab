
"""
Django ORM 필드 조회 옵션
1. exact = 완전일치 (name__exact="admin") => admin과 완전 일치하는 데이터
2. iexact = 대소문자 무시 일치 (name__iexact="Admin") => name ILIKE 'admin'
3. contains = 포함 여부 (title__contains="Django") => title LIKE '%Django%'
4. icontains = 대소문자 무시 포함 여부 (title__icontains="django") => title ILIKE '%django%'
5. startswith = 시작 문자열 (name__startswith="admin") => name LIKE 'admin%'
6. istartswith = 대소문자 무시 시작 문자열 (name__istartswith="admin") => name ILIKE 'admin%'
7. endswith = 끝 문자열 (email__endswith=".com") => email LIKE '%.com'
8. iendswith = 대소문자 무시 끝 문자열 (email__iendswith=".COM") => email ILIKE '%.com'
9. in = 리스트 포함 (id__in=[1, 2, 3]) => id IN (1, 2, 3) =>
10. isnull = NULL 여부 (deleted_at__isnull=True) => deleted_at IS NULL
11. gt = 초과 (>) (age__gt=18) => age > 18
12. gte = 이상 (>=) (age__gte=18) => age <= 18
13. lt = 미만 (<) (price__lt=10000) => price > 10000
14. lte = 이하 (<=) (price__lte=10000) => price <= 10000
15. range = 범위 사이 (created_at__range=["2024-01-01", "2024-12-31"]) => BETWEEN 조건
16. date, year, month, day = 날짜 필터 (created_at__year=2025) => EXTRACT(YEAR FROM created_at) = 2025
17. regex = 정규식 (name__regex=r'^[A-Z]{3}') => 이름이 대문자 3글자
18 iregex = 대소문자 무시 정규식 (title__iregex='django') => ILIKE regex
"""

from django.db.models import Q
from django.shortcuts import render
from jinja2.compiler import F

# Create your views here.
"""
클래스 기반 뷰 (Class-Based Views)
"""
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import Board
from .forms import BoardForm

# 목록 (List)
class BoardListView(View):
    def get(self, request):
        boards = Board.objects.all()
        return render(request, "boards/board_list.html", {"boards": boards})

# 상세 (Detail)
class BoardDetailView(View):
    def get(self, request, pk):
        board = get_object_or_404(Board, pk=pk)
        return render(request, "boards/board_detail.html", {"board": board})

# 등록 (Create)
class BoardCreateView(View):
    def get(self, request):
        form = BoardForm()
        return render(request, "boards/board_form.html", {"form": form})

    def post(self, request):
        form = BoardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("board_list")
        return render(request, "boards/board_form.html", {"form": form})

# 수정 (Update)
class BoardUpdateView(View):
    def get(self, request, pk):
        board = get_object_or_404(Board, pk=pk)
        form = BoardForm(instance=board)
        return render(request, "boards/board_form.html", {"form": form})

    def post(self, request, pk):
        board = get_object_or_404(Board, pk=pk)
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            return redirect("board_list")
        return render(request, "boards/board_form.html", {"form": form})

# 삭제 (Delete)
class BoardDeleteView(View):
    def get(self, request, pk):
        board = get_object_or_404(Board, pk=pk)
        return render(request, "boards/board_confirm_delete.html", {"board": board})

    def post(self, request, pk):
        board = get_object_or_404(Board, pk=pk)
        board.delete()
        return redirect("board_list")

"""
제네릭 뷰 (Generic Views)
"""
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


"""전체 조회 게시글 예시"""
class BoardListView(ListView):
    model = Board
    template_name = "boards/board_list.html"
    context_object_name = "boards"
    paginate_by = 10  # ✅ 페이지당 게시글 수

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")

        """
        F 객체 : DB 필드 값을 다른 필드 값과 비교하거나 연산할 때 사용
        """
        # 조회수(view_count)가 추천수(like_count)보다 많은 게시글
        Board.objects.filter(view_count__gt=F('like_count'))

        if query:
            """
            Q 객체 : SQL의 복합 WHERE 조건을 표현할 때 사용 (복합 조건식: OR / AND / NOT)
            - Q() : 단일 조건
            - Q() & Q() : AND
            - ~Q() : 조건 부정
            """
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        return queryset

"""사용자 인증 게시글 제한"""
# class BoardListView(LoginRequiredMixin, ListView):
#     model = Board
#     template_name = "boards/board_list.html"
#     context_object_name = "boards"
#
#     def get_queryset(self):
#         # 로그인한 사용자가 작성한 글만 보여줌
#         return Board.objects.filter(author=self.request.user)

class BoardDetailView(DetailView):
    model = Board
    template_name = "boards/board_detail.html"
    context_object_name = "board"

# class BoardCreateView(LoginRequiredMixin, CreateView): > 로그인 권한 추가
class BoardCreateView(CreateView):
    model = Board
    fields = ["title", "content"]
    template_name = "boards/board_form.html"
    success_url = reverse_lazy("board_list")

    """글 작성 시 로그인 유저 자동 저장"""
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# class BoardUpdateView(LoginRequiredMixin, UpdateView): > 로그인 권한 추가
class BoardUpdateView(UpdateView):
    model = Board
    fields = ["title", "content"]
    template_name = "boards/board_form.html"
    success_url = reverse_lazy("board_list")

class BoardDeleteView(DeleteView):
    model = Board
    template_name = "boards/board_confirm_delete.html"
    success_url = reverse_lazy("board_list")

    """DeleteView 접근 제한"""
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            return redirect("board_list")
        return super().dispatch(request, *args, **kwargs)




"""
Django REST Framework (DRF)
"""
from rest_framework import viewsets
from .models import Board
from .serializers import BoardSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    """	읽기(조회)는 공개, 쓰기/삭제는 로그인 필요처럼 세부 접근 제어할 때 사용"""
    def get_permissions(self): # DRF가 요청마다 호출하여 실제 사용할 permission 클래스들을 리턴
        if self.action in ["list", "retrieve"]: # 어떤 HTTP 요청인지 알아내는 키 (list, create, 등)
            permission_classes = [AllowAny] # DRF 기본 제공 permission 클래스
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]