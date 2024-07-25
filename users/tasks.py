import datetime
import smtplib
from pytz import timezone
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from config.settings import CELERY_TIMEZONE
from users.models import Subscription, User


@shared_task
def send_sub_mail(course):
    subs_list = Subscription.object.filter(course=course.id)

    try:
        send_mail(
            subject='Изменение статуса курса',
            message=f"Курс {course.name} был изменен",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[sub.user.email for sub in subs_list],
            fail_silently=False,
        )

    except smtplib.SMTPException as e:
        raise e


@shared_task
def check_user():
    for user in User.objects.filter(is_active=True, is_superuser=False, last_login__isnull=False):
        if datetime.datetime.now(timezone(CELERY_TIMEZONE)) - user.last_login > datetime.timedelta(weeks=4):
            user.is_active = False
            user.save()
            print('Пользователь заблокирован')
        else:
            print('Блокировать некого')
