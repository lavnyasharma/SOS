from .token import Token
from ..models import EmailToken
from django.core.mail.message import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site

def send_email(request, email, subject=' ', message=' ',html=' '):
    """
    request
    email
    subject
    message
    html
    """
    mail= EmailMultiAlternatives(subject,message, to=[email])
    if html != ' ':
        mail.attach_alternative(html, 'text/html')
    mail.send()



def email_token():
    try:
        token = Token()
        while 1:
            if EmailToken.objects.filter(Conf_token=token).exists():
                token = Token()
            else:
                return token
    except Exception as e:
        print(e)
        raise Exception("something went wrong")