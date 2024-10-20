from django.contrib.sessions.models import Session
from django.http import HttpRequest, JsonResponse, HttpResponse
import json
from user_moudle.models import User_Sessions
from utils.custom_decoders import Decode_Unity_Cookies
def Auth_Check_Unity(func):
    def To_do(*args,**kwargs):
        request=args[0] or kwargs['request']
        cookie=Decode_Unity_Cookies(request.headers.get('cookie')) or None
        key=cookie['session_id'] or None
        print(cookie)
        if key is not None and User_Sessions.objects.filter(key=key).exists():
            return func(*args,**kwargs)
        else:
            return JsonResponse({'auth_status':['0']})
    return To_do

def Unity_View(func):
    def check_validity(*args,**kwargs):
        request=args[0]
        if request.headers.get('User-Agent') and request.headers.get('User-Agent') == 'UnityPlayer/2020.1.4f1 (UnityWebRequest/1.0, libcurl/7.52.0-DEV)':
            return func(*args,**kwargs)
        else:
            return HttpResponse('Failure',status=403)
    return check_validity
