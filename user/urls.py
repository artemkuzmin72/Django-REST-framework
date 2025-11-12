from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (PaymentCreateAPIView, PaymentListView,
                    PaymentStatusAPIView, SubscriptionAPIView,
                    UserCreateAPIView, UserDestroyAPIView, UserListAPIView,
                    UserRetrieveAPIView, UserUpdateAPIView)

app_name = "user"

urlpatterns = [
    # Платежи
    path("payments/", PaymentListView.as_view(), name="payment-list"),
    path("payments/create/", PaymentCreateAPIView.as_view(), name="payment-create"),
    path(
        "payments/<int:payment_id>/status/",
        PaymentStatusAPIView.as_view(),
        name="payment-status",
    ),
    # JWT токены
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Пользователи
    path("", UserListAPIView.as_view(), name="user-list"),
    path("create/", UserCreateAPIView.as_view(), name="user-create"),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="user-detail"),
    path("update/<int:pk>/", UserUpdateAPIView.as_view(), name="user-update"),
    path("delete/<int:pk>/", UserDestroyAPIView.as_view(), name="user-delete"),
    # Подписки
    path("subscriptions/", SubscriptionAPIView.as_view(), name="subscription-manage"),
]
