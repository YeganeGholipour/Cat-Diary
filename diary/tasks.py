from celery import shared_task
from .models import CatDiary
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_yearly_reminders():
    one_year_ago = datetime.now() - timedelta(days=365)
    entries = CatDiary.objects.filter(date=one_year_ago.date())
    diaries = {}

    for entry in entries:
        if entry.user.email not in diaries:
            diaries[entry.user.email] = []
        diaries[entry.user.email].append(entry)

    for email, diary_entries in diaries.items():
        diary_entries = sorted(diary_entries, key=lambda x: x.date, reverse=True)
        entries_text = "\n".join([f"{d.date} - {d.entry}" for d in diary_entries])
        message = f"Here are your cat's diary entries for the past year:\n\n{entries_text}"
        send_mail(
            subject="Your cat's diary entries for the past year",
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

# tasks.py


@shared_task
def send_test_email():
    send_mail(
        subject="Test email",
        message="This is a test email.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=["yeganegholiour@gmail.com"],
        fail_silently=False,
    )
