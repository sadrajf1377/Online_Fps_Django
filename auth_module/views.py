import json
import random
import string
from random import choices
import datetime

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, Count
from django.shortcuts import render, redirect

# Create your views here.
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, ListView
from rest_framework import generics
from django.middleware.csrf import get_token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from user_moudle.models import custom_user
from utils.Email_Sending import Send_Email_To
# Create your views here.
from .unity_form_validators import Unity_Form_Validate
from user_moudle.models import custom_user,User_Friends_List,User_Block_List
from user_moudle.serializers import User_Serializer

from utils.my_decorators import Auth_Check_Unity
from user_moudle.models import User_Sessions
from utils.custom_decoders import Decode_Unity_Cookies
from utils.my_functions import Check_If_Online
from .forms import Login_Form,SignUp_Form
import re
from news_module.models import News
escaped_chars=re.escape('[!@#$%^&*.?]')
pattern=rf'(?=.*[A-Z].*)(?=.*[a-z].*)(?=.*[0-9].*)(?=.*[{escaped_chars}].*)'
@method_decorator(csrf_protect,name='dispatch')
class genreate_token(View):
    def get(self,request):
        token=get_token(request)
        print('generated token is :',token)
        return JsonResponse(token,safe=False)

class Sign_User_Up(View):
    def post(self,request):
        inst=Unity_Form_Validate()
        act_code = ''.join(choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=72))
        form=inst.Validate_SignUp_Form(post_request= request.POST,act_code=act_code)
        has_errors=(any([value for value in form.values() if len(value)>0]))
        status='succeed' if not has_errors else 'fail'
        contex={'status':[status]}
        if has_errors:
            contex.update(form)
        else:
            rd=request.POST
            br_date=datetime.date(int(rd.get('birth_year')),int(rd.get('birth_month')),int(rd.get('birth_day')))
            new_us=custom_user(username=rd.get('username'),email=rd.get('email'),birth_date=br_date,activation_code=act_code)
            new_us.set_password(request.POST.get('password'))
            new_us.is_active=False
            new_us.save()
        return JsonResponse(contex)

def Activate_User(request,act_code):
    user=custom_user.objects.get(activation_code=act_code)
    user.is_active=True
    user.activation_code=''
    user.save()
    return render(request,'Account_Activated_Message.html',{'username':user.username})


class Log_User_In(View):
    def post(self,request):
        try:
          email_or_username=request.POST.get('username')
          user=custom_user.objects.get(Q(username=email_or_username)|Q(email=email_or_username))
          password=request.POST.get('password')
          if user.check_password(password):
              session=User_Sessions(user_id=user.id)
              session.Assign_key()
              session.save()
              return JsonResponse({'status':'succeed','session_id':session.key})
          else:
              return JsonResponse({'status': 'fail','message':'user not found!'})
        except:
            return JsonResponse({'status': 'fail', 'message': 'user not found!'})

@Auth_Check_Unity
@api_view(['GET'])
def Get_User_info(request):
    if request.method == "GET":

       dict=Decode_Unity_Cookies(request.headers.get('cookie'))
       key=dict['session_id']
       user=custom_user.objects.get(user_sessions__key=key)
       resp=User_Serializer(user,many=False)
       return Response(resp.data,status=200)

def Log_User_Out_Unity(request):
    if request.method =='GET':
        try:
              dict=Decode_Unity_Cookies(request.headers.get('cookie'))
              User_Sessions.objects.get(key=dict['session_id']).delete()
              return JsonResponse({'status':'Logged Out Successfully'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'Session Not Found'})

class User_Login_WebPage(View):
    def get(self,request):
        form=Login_Form()
        print(request.user.is_authenticated)
        return render(request,'Login_Page.html',{'form':form})
    def post(self,request):
        frm=Login_Form(request.POST)
        try:
            if frm.is_valid():
                 user=custom_user.objects.get(username=frm.cleaned_data.get('username'))
                 passw=frm.cleaned_data.get('password')
                 if user.check_password(passw) and user.user_status !='banned':
                     login(request,user)
                     return redirect(reverse('Load_First_Page'))
                 else:
                      frm.add_error('password','User Not Found')
                      return render(request,'Login_Page.html',{'form':frm})
            else:
                return render(request,'Login_Page.html',{'form':frm})
        except:
            return render(request, 'Login_Page.html', {'form': frm})
class User_SignUp_WebPage(View):
    def post(self,request):
        frm=SignUp_Form(request.POST)
        print('ive been called')
        if frm.is_valid():
            email_exists=custom_user.objects.filter(email=frm.cleaned_data.get('email')).exists()
            username_exists=custom_user.objects.filter(email=frm.cleaned_data.get('username')).exists()
            passwords_dont_match=not frm.cleaned_data.get('password') == request.POST.get('password_repeat')
            password_is_weak=not re.match(pattern,frm.cleaned_data.get('password'))
            allowed_to_create=not email_exists and not username_exists and not password_is_weak and not passwords_dont_match
            if allowed_to_create:
                user=frm.save()
                act_code=''.join(random.choices(string.ascii_uppercase+string.ascii_lowercase+string.digits+string.ascii_lowercase
                                                +'[!@#$%^&*.?',k=72))
                user.activation_code=act_code
                Send_Email_To(template_name='User_Activation_Email.html',to=frm.cleaned_data.get('email'),subject='Activate Your Account',contex={})
                user.set_password(frm.cleaned_data.get('password'))
                user.save()
                return render(request,'congrats.html')

            else:
                if email_exists:
                    frm.add_error('email','Such Email Exists')
                if username_exists:
                    frm.add_error('username','Such Username exists')
                if passwords_dont_match:
                    frm.add_error('password','Passwords dont match')
                if password_is_weak:
                    frm.add_error('password','password must contain one uppercharacter,one number and one special character')
            return render(request, 'Sign_Up.html', {'form': frm})

        else:
            return render(request,'Sign_Up.html',{'form':frm})
    def get(self,request):
        form=SignUp_Form()
        return render(request,'Sign_Up.html',{'form':form})

@method_decorator(login_required,name='dispatch')
class Load_First_Page(ListView):
    template_name = 'User_Panel.html'
    model = News
    paginate_by = 6
    ordering = 'creation_date'
    context_object_name = 'news'
    def get_context_data(self, *, object_list=None, **kwargs):
        user:custom_user=self.request.user
        friends_list=user.get_friends_list()
        block_list=user.get_block_list()
        top_players=custom_user.objects.order_by('-user_total_score').all()[:8]
        contex=super().get_context_data()
        contex.update({'block_list':block_list,'friends_list':friends_list,'top_players':top_players})
        return contex
    def get_queryset(self):
        query_set=super().get_queryset()
        query_set=query_set.annotate(likes=Count('news_comments',filter=Q(news_comments__like_or_dislike='like')))
        query_set=query_set.annotate(dislikes=Count('news_comments',filter=Q(news_comments__like_or_dislike='dislike')))

        return query_set
class Log_User_Out_WebPage(View):
    def get(self,request):
        logout(request)
        return redirect(reverse('Load_First_Page'))
class Search_Users(View):
    def get(self,request):
        inp=request.GET.get('inp_name')
        print(request.GET)
        users=custom_user.objects.filter(username__contains=inp)[:6]
        users=[[x.username,x.get_avatar()] for x in users]
        return JsonResponse({'matching_users':users})