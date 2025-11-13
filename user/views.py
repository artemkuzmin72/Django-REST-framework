from decimal import Decimal

import stripe
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course
from materials.service import (
    create_stripe_price,
    create_stripe_product,
    create_stripe_session,
    retrieve_stripe_session,
)

from .models import Payment, Subscription, User
from .serializers import PaymentSerializer, UserSerializer


class PaymentListView(generics.ListAPIView):
    """List of Payments with filtering and ordering"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    filterset_fields = {
        "course": ["exact"],
        "lesson": ["exact"],
        "payment_method": ["exact"],
        "payment_date": ["exact", "gte", "lte"],
    }

    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]


class UserCreateAPIView(generics.CreateAPIView):
    """User Create"""

    serializer_class = UserSerializer


class UserListAPIView(generics.ListAPIView):
    """User List"""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """User Detail"""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    """User Update"""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(generics.DestroyAPIView):
    """User Delete"""

    queryset = User.objects.all()


class SubscriptionAPIView(APIView):
    """
    - Если пользователь уже подписан на курс удаляет подписку.
    - Если нет создает новую.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")

        if not course_id:
            return Response({"error": "Поле 'course_id' обязательно."}, status=400)

        course = get_object_or_404(Course, id=course_id)

        subscription_qs = Subscription.objects.filter(user=user, course=course)

        if subscription_qs.exists():
            subscription_qs.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message})


class PaymentCreateAPIView(APIView):
    """
    Создание платежа через Stripe.
    Принимает course_id и создает продукт, цену и сессию в Stripe.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")

        if not course_id:
            return Response({"error": "Поле 'course_id' обязательно."}, status=400)

        course = get_object_or_404(Course, id=course_id)

        # Получаем сумму из курса (предполагаем, что цена хранится в курсе)
        # Если цены нет в модели курса, можно передать amount в запросе
        amount = request.data.get("amount")
        if not amount:
            return Response({"error": "Поле 'amount' обязательно."}, status=400)

        try:
            amount = Decimal(str(amount))
        except (ValueError, TypeError):
            return Response({"error": "Некорректная сумма."}, status=400)

        try:
            # Создаем продукт в Stripe
            product_data = create_stripe_product(
                name=course.title,
                description=course.description or "",
            )

            # Создаем цену в Stripe
            price_data = create_stripe_price(
                product_id=product_data["id"],
                amount=float(amount),
            )

            # Формируем URLs для редиректа
            base_url = request.build_absolute_uri("/")[:-1]  # Убираем последний слеш
            success_url = f"{base_url}/user/payments/success/"
            cancel_url = f"{base_url}/user/payments/cancel/"

            # Создаем сессию в Stripe
            session_data = create_stripe_session(
                price_id=price_data["id"],
                success_url=success_url,
                cancel_url=cancel_url,
            )

            # Создаем платеж в нашей системе
            payment = Payment.objects.create(
                user=user,
                course=course,
                amount=amount,
                payment_method=Payment.STRIPE,
                status=Payment.STATUS_PENDING,
                stripe_product_id=product_data["id"],
                stripe_price_id=price_data["id"],
                stripe_session_id=session_data["id"],
                payment_url=session_data["url"],
            )

            serializer = PaymentSerializer(payment)
            return Response(serializer.data, status=201)
        except stripe.error.StripeError as e:
            return Response({"error": f"Ошибка Stripe: {str(e)}"}, status=400)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)
        except Exception as e:
            return Response({"error": f"Неожиданная ошибка: {str(e)}"}, status=500)


class PaymentStatusAPIView(APIView):
    """
    Проверка статуса платежа через Stripe.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, payment_id, *args, **kwargs):
        user = request.user
        payment = get_object_or_404(Payment, id=payment_id, user=user)

        if not payment.stripe_session_id:
            return Response({"error": "Платеж не связан со Stripe."}, status=400)

        # Получаем статус из Stripe
        session_data = retrieve_stripe_session(payment.stripe_session_id)

        if not session_data:
            return Response(
                {"error": "Не удалось получить статус платежа."}, status=400
            )

        # Обновляем статус платежа
        if session_data["payment_status"] == "paid":
            payment.status = Payment.STATUS_PAID
            from django.utils import timezone

            payment.payment_date = timezone.now()
        elif session_data["payment_status"] == "unpaid":
            payment.status = Payment.STATUS_PENDING
        else:
            payment.status = Payment.STATUS_FAILED

        payment.save()

        serializer = PaymentSerializer(payment)
        return Response(serializer.data)
