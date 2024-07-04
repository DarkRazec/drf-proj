from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
                  path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
                  path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
                  path('lesson/<int:pk>', LessonRetrieveAPIView.as_view(), name='lesson-get'),
                  path('lesson/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),
                  path('lesson/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
              ] + router.urls