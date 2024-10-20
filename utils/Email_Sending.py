from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from Online_Game_Server.settings import EMAIL_HOST
import re

def Send_Email_To(template_name,subject,to,contex):
    mes=render_to_string(template_name,contex)
    plain_message=strip_tags(mes)
    sender=EMAIL_HOST
    pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.match(pat,to):
        result='invalid'
    else:
        try:
            send_mail(subject=subject, from_email=sender, recipient_list=[to], message=plain_message,
                               html_message=mes)
            result='succeed'
        except:
            result='fail'
    return result