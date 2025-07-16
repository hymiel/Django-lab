from django.shortcuts import render

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


class BoardListView(ListView):
    model = Board
    template_name = "boards/board_list.html"
    context_object_name = "boards"

class BoardDetailView(DetailView):
    model = Board
    template_name = "boards/board_detail.html"
    context_object_name = "board"

class BoardCreateView(CreateView):
    model = Board
    fields = ["title", "content"]
    template_name = "boards/board_form.html"
    success_url = reverse_lazy("board_list")

class BoardUpdateView(UpdateView):
    model = Board
    fields = ["title", "content"]
    template_name = "boards/board_form.html"
    success_url = reverse_lazy("board_list")

class BoardDeleteView(DeleteView):
    model = Board
    template_name = "boards/board_confirm_delete.html"
    success_url = reverse_lazy("board_list")

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