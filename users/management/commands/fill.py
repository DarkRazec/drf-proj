import json

from django.core.management import BaseCommand

from materials.models import Course, Lesson
from users.models import User, Payment


class Command(BaseCommand):

    @staticmethod
    def json_read_payments():
        # Получаем данные из фикстур с продуктами
        with open('data/payments_data.json', encoding='utf-16') as f:
            return json.load(f)

    def handle(self, *args, **options):

        Payment.objects.all().delete()

        payments_for_create = [Payment(
            id=payment['pk'],
            date=payment['fields']['date'],
            course=Course.objects.get(pk=payment['fields']['course']) if payment['fields']['course'] else None,
            lesson=Lesson.objects.get(pk=payment['fields']['lesson']) if payment['fields']['lesson'] else None,
            user=User.objects.get(pk=payment['fields']['user']),
            sum=payment['fields']['sum'],
            is_card=payment['fields']['is_card'],
        ) for payment in Command.json_read_payments()]

        Payment.objects.bulk_create(payments_for_create)
