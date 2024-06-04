from django.urls import path, include
from .views import ListDiary

urlpatterns = [
    path('create_diary/',ListDiary.as_view(), name="create_diary"),
    path("list_diary/", ListDiary.as_view(), name="list_diary"),
    path("diary_by_date/", ListDiary.as_view(), name="diary_by_date"),
]