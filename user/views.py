from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from user.models import Payments
from .serializers import PaymentSerializer

class PaymentListView(generics.ListAPIView):
    queryset = Payments.objects.all()
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