from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from user.models import Subscription
from user.tasks import send_course_update_email
from .models import Course, Lesson
from .paginators import MyPagination
from .permissions import IsModerator, IsModeratorOrReadOnly, IsOwner
from .serializers import CourseSerializer, LessonSerializer

# Create your views here.


class CourseViewSet(viewsets.ModelViewSet):
    """CRUD для курсов"""

    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated & IsModeratorOrReadOnly | IsOwner]
    pagination_class = MyPagination
    queryset = Course.objects.all()

    def get(self, request, queryset):
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = CourseSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user
        if user.groups.filter(name="Модераторы").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def perform_update(self, serializer):
        """
        При обновлении курса отправляем уведомления подписчикам.
        """
        course = serializer.save()

        # Находим всех подписанных пользователей
        subscriptions = Subscription.objects.filter(course=course)
        emails = [sub.user.email for sub in subscriptions if sub.user.email]

        # Вызываем асинхронную задачу
        if emails:
            send_course_update_email.delay(course.title, emails)

    def get_serializer_context(self):
        """
        Передаем request в сериализатор, чтобы можно было узнать текущего пользователя.
        """
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class LessonCreateAPIView(generics.CreateAPIView):
    """Lesson Create"""

    permission_classes = [IsAuthenticated & IsModerator]
    serializer_class = LessonSerializer
    pagination_class = MyPagination

    def get_queryset(self):
        return Lesson.objects.all()

    def get_permissions(self):
        # Allow anyone to view (read-only). Require authentication to create.
        if self.request and self.request.method == "POST":
            return [IsAuthenticated()]
        return [IsModeratorOrReadOnly()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    """Lesson List"""

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & IsModeratorOrReadOnly]
    pagination_class = MyPagination

    def get(self, request):
        queryset = Lesson.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = LessonSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Lesson Detail"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated & IsModeratorOrReadOnly | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Lesson Update"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated & IsModeratorOrReadOnly | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Lesson Deleteç"""

    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated | IsOwner]
