from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render,redirect
def sent_mail_to_client(user_email=None,user_name=None,user_message=None):
  if(user_email==None or user_name==None or user_message==None):
    subject = 'Test Email'
    message = user_message
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)
    return redirect('http://127.0.0.1:8000/home/')
  else:
    subject="Contact Email"
    message=user_message
    from_email = settings.EMAIL_HOST_USER
    recipient_list=[user_email]
    print("ok")
    send_mail(subject,message,from_email,recipient_list)
    print("email sent")

# def sent_mail_to_client(user_email=None,user_name=None,user_message=):

#     subject = 'Test Email'
#     message = 'This is a test email sent using Django.'
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = [user_email]
#     send_mail(subject, message, from_email, recipient_list)
#     return redirect('http://127.0.0.1:8000/home/')
