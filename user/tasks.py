from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from user.models import User


@shared_task
def send_course_update_email(course_title, emails):
    """
    Асинхронная рассылка писем подписчикам курса
    """
    subject = f"Обновление курса: {course_title}"
    message = f"Курс '{course_title}' был обновлён. Проверьте новые материалы!"

    send_mail(
        subject,
        message,
        emails,
        fail_silently=False,
    )


@shared_task
def deactivate_inactive_users():
    """
    Деактивирует пользователей, не заходивших более 30 дней.
    """
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)

    count = inactive_users.update(is_active=False)
    print(f"{count} пользователей деактивировано (неактивны более 30 дней)")
    return count
