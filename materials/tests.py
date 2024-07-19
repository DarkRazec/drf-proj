from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Lesson, Course
from users.models import User, Subscription


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='admin@admin')
        self.client.force_authenticate(user=self.user)
        self.data = {
            "name": "test",
            "desc": "test",
            "url": "https://www.youtube.com/",
        }
        self.test_obj = Lesson.objects.create(**self.data, author=self.user)

    def test_create_lesson(self):
        response = self.client.post(
            '/lessons/create/',
            data=self.data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {
                "id": 2,
                "name": "test",
                "desc": "test",
                "url": "https://www.youtube.com/",
                "author": 1,
                "preview": None,
                "course": None
            }
        )

        self.assertTrue(
            Lesson.objects.all().exists()
        )

    def test_list_lessons(self):
        response = self.client.get(
            '/lessons/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            [{
                "id": 1,
                "name": "test",
                "desc": "test",
                "url": "https://www.youtube.com/",
                "author": 1,
                "preview": None,
                "course": None
            }]
        )

    def test_update_lessons(self):
        new_data = {
            "id": 1,
            "name": "test2",
            "desc": "test2",
            "url": "https://www.youtube.com/",
            "author": 1,
        }

        response = self.client.patch(
            '/lessons/1/update/',
            data=new_data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "id": 1,
                "name": "test2",
                "desc": "test2",
                "url": "https://www.youtube.com/",
                "author": 1,
                "preview": None,
                "course": None
            }
        )


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='admin@admin')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            name="test",
            desc="test",
        )
        self.data = {
            "user": self.user.id,
            "course": self.course.id,
        }

    def test_subscription_activate(self):
        """Тест активации подписки"""
        response = self.client.post(
            '/subscriptions/',
            data=self.data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "message": "Подписка добавлена",
            },
        )

        self.assertTrue(
            Subscription.objects.all().exists(),
        )

    def test_sub_deactivate(self):
        """Тест дективации подписки"""
        Subscription.objects.create(user=self.user, course=self.course)

        response = self.client.post(
            '/subscriptions/',
            data=self.data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.json(),
            {
                "message": "Подписка удалена",
            },
        )

        self.assertFalse(
            Subscription.objects.all().exists(),
        )
