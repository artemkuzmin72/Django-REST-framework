from django.core.management.base import BaseCommand
from django.utils import timezone

from materials.models import Course, Lesson
from user.models import Payment, User


class Command(BaseCommand):
    help = "Создаёт тестовые платежи"

    def handle(self, *args, **kwargs):
        user = User.objects.first()
        course = Course.objects.first()
        lesson = Lesson.objects.first()

        if not user:
            self.stdout.write(self.style.ERROR("Нет пользователей в базе!"))
            return

        Payment.objects.create(
            user=user,
            payment_date=timezone.now(),
            course=course,
            amount=1500.00,
            payment_method="cash",
        )

        Payment.objects.create(
            user=user,
            payment_date=timezone.now(),
            lesson=lesson,
            amount=700.00,
            payment_method="transfer",
        )

        self.stdout.write(self.style.SUCCESS("Данные о платежах успешно добавлены!"))
