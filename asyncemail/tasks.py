from celery import shared_task
from django.conf import settings
from time import sleep

from django.core.mail import send_mail
# lets demonstrate how celery is asynchronous
# decorator
@shared_task
def sleepy(duration):
    sleep(duration)
    return None


@shared_task
def send_email_task():
    sleep(10)
    send_mail("celery works",
          "this is great", settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
    return None

