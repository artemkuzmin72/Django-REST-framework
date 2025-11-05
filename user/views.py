from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from user.models import Payment, User
from .serializers import PaymentSerializer, UserSerializer

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
    serializer_class = UserSerializer()

class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer()
    queryset = User.objects.all()

class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer()
    queryset = User.objects.all()

class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer()
    queryset = User.objects.all()

class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()