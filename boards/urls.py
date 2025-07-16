from django.shortcuts import render

# Create your views here.
"""
클래스 기반 뷰 (Class-Based Views)
"""
from django.urls import path
from .views import *

urlpatterns = [
    path("", BoardListView.as_view(), name="board_list"),
    path("<int:pk>/", BoardDetailView.as_view(), name="board_detail"),
    path("create/", BoardCreateView.as_view(), name="board_create"),
    path("<int:pk>/edit/", BoardUpdateView.as_view(), name="board_update"),
    path("<int:pk>/delete/", BoardDeleteView.as_view(), name="board_delete"),
]

"""
제네릭 뷰 (Generic Views)
"""
from django.urls import path
from .views import *

urlpatterns = [
    path("", BoardListView.as_view(), name="board_list"),
    path("<int:pk>/", BoardDetailView.as_view(), name="board_detail"),
    path("create/", BoardCreateView.as_view(), name="board_create"),
    path("<int:pk>/edit/", BoardUpdateView.as_view(), name="board_update"),
    path("<int:pk>/delete/", BoardDeleteView.as_view(), name="board_delete"),
]

"""
Django REST Framework (DRF)
"""
from rest_framework.routers import DefaultRouter
from .views import BoardViewSet

router = DefaultRouter()
router.register("boards", BoardViewSet, basename="board")

urlpatterns = router.urls
