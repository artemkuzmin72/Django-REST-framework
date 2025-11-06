from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from materials.models import Course, Lesson
from user.models import Subscription

User = get_user_model()


class LessonAndSubscriptionTestCase(APITestCase):
    """
    Тесты CRUD для уроков и функционала подписки на курс.
    """

    def setUp(self):
        # Пользователи
        self.user = User.objects.create_user(email='user@example.com', password='userpass')
        self.moderator = User.objects.create_user(email='moderator@example.com', password='modpass')
        self.admin = User.objects.create_superuser(email='admin@example.com', password='adminpass')

        # Создаём курс
        self.course = Course.objects.create(title="Python Base", description="Основы Python", owner=self.admin)

        # Создаём урок
        self.lesson = self.course.lessons.create(
            title="Урок 1",
            description="Введение в Python",
            link="https://youtube.com/watch?v=test",
            owner=self.admin
        )

        self.client = APIClient()

        # URL для уроков
        self.lesson_list_url = reverse('lesson-list')
        self.lesson_detail_url = reverse('lesson-detail', args=[self.lesson.id])

        # URL для подписки
        self.subscription_url = reverse('subscription')

    def test_lesson_list_guest(self):
        """Гость может просматривать список уроков."""
        response = self.client.get(self.lesson_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_create_authenticated_user(self):
        """Авторизованный пользователь может создавать уроки."""
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "Урок 2",
            "description": "https://youtube.com/watch?v=abc",
            "course": self.course.id
        }
        response = self.client.post(self.lesson_list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Урок 2")

    def test_lesson_update_owner(self):
        """Создатель урока может редактировать его."""
        self.client.force_authenticate(user=self.admin)
        data = {"title": "Обновлённый урок"}
        response = self.client.patch(self.lesson_detail_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Обновлённый урок")

    def test_lesson_delete_not_allowed_for_user(self):
        """Обычный пользователь не может удалять чужие уроки."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.lesson_detail_url)
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED])

    # ----------------------- TEST SUBSCRIPTION -----------------------------

    def test_create_subscription(self):
        """Пользователь может подписаться на курс."""
        self.client.force_authenticate(user=self.user)
        data = {"course_id": self.course.id}
        response = self.client.post(self.subscription_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка добавлена")

        # Проверяем, что запись появилась в базе
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_remove_subscription(self):
        """Если подписка уже есть — повторный POST удаляет её."""
        Subscription.objects.create(user=self.user, course=self.course)

        self.client.force_authenticate(user=self.user)
        data = {"course_id": self.course.id}
        response = self.client.post(self.subscription_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка удалена")

        # Проверяем, что запись удалена
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscription_field_in_course_detail(self):
        """В API по курсу возвращается поле is_subscribed."""
        self.client.force_authenticate(user=self.user)
        Subscription.objects.create(user=self.user, course=self.course)

        url = reverse('course-detail', args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_subscribed"])

    def test_subscription_field_for_unsubscribed_user(self):
        """Поле is_subscribed = False, если пользователь не подписан."""
        self.client.force_authenticate(user=self.user)
        url = reverse('course-detail', args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["is_subscribed"])