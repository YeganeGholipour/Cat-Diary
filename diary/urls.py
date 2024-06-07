from django.urls import path, include
from .views import ListDiary, SendEmailView, DiaryEntryByDate

urlpatterns = [
    path('create_diary/',ListDiary.as_view(), name="create_diary"),
    path("list_diary/", ListDiary.as_view(), name="list_diary"),
    path("diary_by_date/", DiaryEntryByDate.as_view(), name="diary_by_date"),
    path('send-email/', SendEmailView.as_view(), name='send-email'),
]