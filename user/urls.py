from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PaymentListView, UserListAPIView, UserCreateAPIView, UserRetrieveAPIView, UserUpdateAPIView, UserDestroyAPIView, SubscriptionAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from user.apps import UserConfig

app_name = UserConfig.name

urlpatterns = [
    path('payments/', PaymentListView.as_view(), name='payment_list'),

    path("token/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),

    path('create/', UserCreateAPIView.as_view(), name='user-create'),
    path(" ", UserListAPIView.as_view(), name='User-list'),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name='User-get'),
    path("update/<int:pk>/", UserUpdateAPIView.as_view(), name='User-update'),
    path("delete/<int:pk>/", UserDestroyAPIView.as_view(), name='User-delete'),

    path("subscriptions/", SubscriptionAPIView.as_view(), name="subscription_manage"),
]
