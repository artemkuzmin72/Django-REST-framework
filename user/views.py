from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment, User, Subscription
from .serializers import PaymentSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from materials.models import Course
from rest_framework.views import APIView

class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    filterset_fields = {
        'course': ['exact'],
        'lesson': ['exact'],
        'payment_method': ['exact'],
        'payment_date': ['exact', 'gte', 'lte'], 
    }

    ordering_fields = ['payment_date']
    ordering = ['-payment_date']  

class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserDestroyAPIView(generics.DestroyAPIView):
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