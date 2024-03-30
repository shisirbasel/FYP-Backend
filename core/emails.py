from django.core.mail import send_mail
import random
from django.conf import settings
from core.models import User
from celery import shared_task

@shared_task
def send_otp(email):
    subject = 'Your account verfication email'
    otp = random.randint(1000,9999)
    message = f'Your otp is {otp}'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject,message,email_from,[email])
    user_obj = User.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()




