from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson
from materials.paginators import MaterialsPaginator
from users.models import Subscription
from users.permissions import IsStaff, IsAuthor
from materials.serializer import CourseSerializer, LessonSerializer, SubscriptionSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = MaterialsPaginator

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
    pagination_class = MaterialsPaginator

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


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course = generics.get_object_or_404(Course, pk=self.request.data.get('course'))

        subscription, created = Subscription.objects.get_or_create(user=user, course=course)
        if created:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'
        else:
            subscription.delete()
            message = 'Подписка удалена'

        return Response({"message": message})
