from django.core.mail import EmailMessage,send_mail
import random
from django.conf import settings
from core.models import User

def send_otp(email):
    subject = 'Your account verfication email'
    otp = random.randint(1000,9999)
    message = f'Your otp is {otp}'
    email_from = settings.EMAIL_HOST_USER
    # send_mail(subject,message,email_from,[email])
    email = EmailMessage(subject,message,email_from,[email])
    email.fail_silently = True
    email.send()
    
    # return verify_otp(otp, user_input)

def verify_otp(otp,user_input):
    if otp == user_input:
        return True
    return False

