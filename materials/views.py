from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from users.permissions import IsStaff, IsAuthor
from materials.serializer import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        self.object = serializer.save()
        self.object.author = self.request.user
        self.object.save()

    def get_permissions(self):
        if self.action in ('create', 'destroy'):
            permission_classes = [~IsStaff, IsAuthor]
        elif self.action in ('update', 'retrieve'):
            permission_classes = [IsStaff | IsAuthor]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~IsStaff, IsAuthenticated]

    def perform_create(self, serializer):
        self.object = serializer.save()
        self.object.author = self.request.user
        self.object.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsStaff | IsAuthor]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsStaff | IsAuthor]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [~IsStaff, IsAuthor]
