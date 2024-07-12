from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from materials.models import Course, Lesson


class Command(BaseCommand):
    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='moderator')
        if created:
            content_type = ContentType.objects.get_for_model(Course)
            group.permissions.add(Permission.objects.get(codename='view_course', content_type=content_type))
            group.permissions.add(Permission.objects.get(codename='change_course', content_type=content_type))
            content_type = ContentType.objects.get_for_model(Lesson)
            group.permissions.add(Permission.objects.get(codename='view_lesson', content_type=content_type))
            group.permissions.add(Permission.objects.get(codename='change_lesson', content_type=content_type))
            group.save()
            print('Группа создана')
        else:
            print('Группа уже существует')
