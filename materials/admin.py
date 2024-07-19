from django.contrib import admin

from materials.models import Course, Lesson
from users.models import Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc', 'author',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc', 'author',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'course']
