from django.urls import path
<<<<<<< HEAD
from .views import (
    PaymentListView,
    UserListAPIView,
    UserCreateAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
    UserDestroyAPIView,
    SubscriptionAPIView,
=======
from rest_framework.routers import DefaultRouter
from .views import PaymentListView, UserListAPIView, UserCreateAPIView, UserRetrieveAPIView, UserUpdateAPIView, UserDestroyAPIView, SubscriptionAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
>>>>>>> 60d81ba030f417047f72c225d9b2a514b09cc5e5
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'user'

urlpatterns = [
    # Платежи
    path('payments/', PaymentListView.as_view(), name='payment-list'),

    # JWT токены
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Пользователи
    path('', UserListAPIView.as_view(), name='user-list'),
    path('create/', UserCreateAPIView.as_view(), name='user-create'),
<<<<<<< HEAD
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user-detail'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user-update'),
    path('delete/<int:pk>/', UserDestroyAPIView.as_view(), name='user-delete'),

    # Подписки
    path('subscriptions/', SubscriptionAPIView.as_view(), name='subscription-manage'),
]
=======
    path(" ", UserListAPIView.as_view(), name='User-list'),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name='User-get'),
    path("update/<int:pk>/", UserUpdateAPIView.as_view(), name='User-update'),
    path("delete/<int:pk>/", UserDestroyAPIView.as_view(), name='User-delete'),

    path("subscriptions/", SubscriptionAPIView.as_view(), name="subscription_manage"),
]
>>>>>>> 60d81ba030f417047f72c225d9b2a514b09cc5e5
