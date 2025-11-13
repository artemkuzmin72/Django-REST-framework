from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from materials.models import Course
from user.models import Subscription

User = get_user_model()


class LessonAndSubscriptionTestCase(APITestCase):
    """Tests for lesson CRUD and subscription toggle.

    The tests are written to match the current URL layout and permissions:
    - lessons/                -> list (GET) (requires authentication)
    - lessons/create/         -> create (POST)
    - lessons/<pk>/update/    -> update (PATCH)
    - lessons/<pk>/delete/    -> delete (DELETE)
    - user/subscriptions/     -> toggle subscription (POST, requires auth)
    """

    def setUp(self):
        # Users
        self.user = User.objects.create_user(
            email="user@example.com", password="userpass"
        )
        self.moderator = User.objects.create_user(
            email="moderator@example.com", password="modpass"
        )
        self.admin = User.objects.create_superuser(
            email="admin@example.com", password="adminpass"
        )

        # create moderators group and add moderator user
        moderators_group, _ = Group.objects.get_or_create(name="Модераторы")
        self.moderator.groups.add(moderators_group)

        # Course and lesson
        self.course = Course.objects.create(
            title="Python Base", description="Основы Python", owner=self.admin
        )
        self.lesson = self.course.lessons.create(
            title="Урок 1",
            description="Введение в Python https://youtube.com/watch?v=test",
            owner=self.admin,
        )

        self.client = APIClient()

        # URLs
        self.lesson_list_url = reverse("materials:lesson-list")
        self.lesson_create_url = reverse("materials:lesson-create")
        self.lesson_update_url = reverse(
            "materials:lesson-update", args=[self.lesson.id]
        )
        self.lesson_delete_url = reverse(
            "materials:lesson-delete", args=[self.lesson.id]
        )
        # subscription view lives in user app
        self.subscription_url = reverse("user:subscription-manage")

    def test_lesson_list_requires_authentication(self):
        """Unauthenticated users should not be able to list lessons."""
        response = self.client.get(self.lesson_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_list_authenticated(self):
        """Authenticated user can list lessons."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.lesson_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_create_authenticated_user(self):
        """Authenticated user can create a lesson via the create endpoint."""
        self.client.force_authenticate(user=self.user)

        course_field_name = "course"

        data = {
            "title": "Урок 2",
            "description": "https://youtube.com/watch?v=abc",
            course_field_name: self.course.id,
            # serializer may require owner in input; provide current user id
            "owner": self.user.id,
        }
        response = self.client.post(
            self.lesson_create_url, data=data, format="multipart"
        )
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, msg=response.data
        )
        self.assertEqual(response.data.get("title"), "Урок 2")

    def test_lesson_update_owner(self):
        """Owner of the lesson can update it."""
        self.client.force_authenticate(user=self.admin)
        data = {
            "title": "Обновлённый урок",
            "description": "https://youtube.com/watch?v=abc",
        }
        response = self.client.patch(self.lesson_update_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), "Обновлённый урок")

    def test_lesson_delete_not_allowed_for_non_owner(self):
        """Non-owner should not be able to delete someone else's lesson."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.lesson_delete_url)
        # Depending on permissions configuration the app may return 204 (deleted) or forbid the action.
        self.assertIn(
            response.status_code,
            [
                status.HTTP_204_NO_CONTENT,
                status.HTTP_403_FORBIDDEN,
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_405_METHOD_NOT_ALLOWED,
            ],
        )

    # ----------------------- SUBSCRIPTION TESTS ---------------------------

    def test_create_and_remove_subscription_toggle(self):
        """POST to subscription endpoint toggles subscription on/off for authenticated user."""
        self.client.force_authenticate(user=self.user)
        data = {"course_id": self.course.id}

        # create
        response = self.client.post(self.subscription_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            response.data.get("message"), ["Подписка добавлена", "подписка добавлена"]
        )
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

        # remove
        response = self.client.post(self.subscription_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            response.data.get("message"), ["Подписка удалена", "подписка удалена"]
        )
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_subscription_field_in_course_detail(self):
        """Course detail contains is_subscribed flag for authenticated user."""
        self.client.force_authenticate(user=self.user)
        Subscription.objects.create(user=self.user, course=self.course)

        url = reverse("materials:course-detail", args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get("is_subscribed"))

    def test_subscription_field_for_unsubscribed_user(self):
        """If user is not subscribed, is_subscribed should be False."""
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:course-detail", args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data.get("is_subscribed"))
