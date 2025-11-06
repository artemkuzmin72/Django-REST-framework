from rest_framework import viewsets, generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsModeratorOrReadOnly, IsModeratorOrOwner, IsOwner, IsModerator
# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated & IsModeratorOrReadOnly | IsOwner]

    def perform_create(self, serializer):
        """
        Привязывает курс к текущему пользователю при создании
        """
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        - Модератор видит все курсы
        - Обычный пользователь — только свои
        """
        user = self.request.user
        if user.groups.filter(name='Модераторы').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

class LessonCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated & IsModerator]
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated & IsModeratorOrReadOnly]

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated & IsModeratorOrReadOnly | IsOwner]

class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated & IsModeratorOrReadOnly | IsOwner]

class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated | IsOwner]
