from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiExample
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson
from materials.paginators import MaterialsPaginator
from users.models import Subscription
from users.permissions import IsStaff, IsAuthor
from materials.serializer import CourseSerializer, LessonSerializer, SubscriptionSerializer
from users.tasks import send_sub_mail


@extend_schema_view(
    list=extend_schema(
        summary="Get course list",
    ),
    update=extend_schema(
        summary="Update for existing course",
    ),
    partial_update=extend_schema(
        summary="Partial update for existing course",
    ),
    create=extend_schema(
        summary="Creating new course",
        examples=[
            OpenApiExample(
                "Course example",
                description="Test example for the course",
                value=
                {
                    "name": "test",
                    "desc": "test",
                },
                status_codes=[str(status.HTTP_201_CREATED)],
            ),
        ],
    ),
    retrieve=extend_schema(
        summary="Course detail info",
    ),
    destroy=extend_schema(
        summary="Delete existing course",
    ),
)
class CourseViewSet(viewsets.ModelViewSet):
    """
        ViewSet for Course models
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = MaterialsPaginator

    def perform_create(self, serializer):
        self.object = serializer.save()
        self.object.author = self.request.user
        self.object.save()

    def perform_update(self, serializer):
        self.object = serializer.save()
        send_sub_mail(self.object)
        self.object.save()

    def get_permissions(self):
        if self.action in ('create', 'destroy'):
            permission_classes = [~IsStaff, IsAuthor]
        elif self.action in ('update', 'retrieve'):
            permission_classes = [IsStaff | IsAuthor]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


@extend_schema(
    summary="Test description of retrieve method",
    examples=[
        OpenApiExample(
            "Course example",
            description="Test example for the course",
            value=
            {
                "name": "test",
                "desc": "test",
                "url": "https://www.youtube.com/"
            },
            status_codes=[str(status.HTTP_201_CREATED)],
        ),
    ],
)
class LessonCreateAPIView(generics.CreateAPIView):
    """
    Lesson create view
    """
    serializer_class = LessonSerializer
    permission_classes = [~IsStaff, IsAuthenticated]
    pagination_class = MaterialsPaginator

    def perform_create(self, serializer):
        self.object = serializer.save()
        self.object.author = self.request.user
        self.object.save()


class LessonListAPIView(generics.ListAPIView):
    """
        Lesson list view
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
        Lesson detail view
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsStaff | IsAuthor]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
        Lesson update view
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsStaff | IsAuthor]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
        Lesson delete view
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [~IsStaff, IsAuthor]


class SubscriptionAPIView(APIView):
    """
        Subscription create view
    """
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
