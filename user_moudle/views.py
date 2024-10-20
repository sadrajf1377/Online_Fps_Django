import json
import random
import string

from django.db.models import Count, Q, Case, When
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views import View
from django.views.generic import UpdateView, ListView, DetailView
from psycopg2.extensions import JSON

from .models import User_Settings, custom_user,Block_List,Friend_Request,User_Friends_List,Friends_List,User_Block_List,User_Report_List

from messages_module.models import Message_Groups,Message
from .forms import Report_Form,Password_Reset_Form
from utils.Email_Sending import Send_Email_To
from post_module.models import Post_Model,Post_Comment
# Create your views here.

class Update_User_Settings(UpdateView):
    template_name = 'User_Dashboard_Base.html'
    success_url = reverse_lazy('update_user_settings')
    model=User_Settings
    fields = '__all__'
    context_object_name = 'form'
    def get_object(self, queryset=None):
        object=self.request.user.get_settings()
        return object
    def get_context_data(self, **kwargs):
        contex=super().get_context_data()
        contex['title']='settings'
        return contex
class Update_Profile(UpdateView):
    model = custom_user
    template_name = 'User_Dashboard_Base.html'
    success_url = reverse_lazy('update_user_profile')
    fields = ['username','first_name','last_name','email','avatar']
    context_object_name = 'form'
    def get_object(self, queryset=None):
        object=custom_user.objects.get(id=self.request.user.id)
        return object
    def get_context_data(self, **kwargs):
        contex=super().get_context_data()
        contex['title']='profile'
        return contex
    def post(self,request:HttpRequest):
        if request.FILES.get('avatar') == None:

            obj:custom_user=self.get_object()
            obj.avatar.delete()
            obj.save()
            print(obj.avatar)
        return super().post(request)
class Get_Block_list(ListView):
    model = custom_user
    template_name = 'User_Dashboard_Base.html'
    context_object_name = 'users'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        contex=super().get_context_data()
        user:custom_user=self.request.user
        user.user_block_list.user_list.users
        contex['title']='blocked_users'
        return contex
    def get_queryset(self):
        querey_set=super().get_queryset()
        user:custom_user=self.request.user
        #custom_user.objects.filter(block_list=user.user_block_list.user_list)
        querey_set=querey_set.filter(block_list=user.user_block_list.user_list)
        print(querey_set)
        return querey_set
class Show_User_Profile(ListView):
    template_name = 'User_Profile.html'
    context_object_name = 'posts'
    model = Post_Model
    paginate_by = 6
    def __init__(self):
        self.target_user=''
        super().__init__()
    def get_ordering(self):
        to_do=self.kwargs['to_do']
        order='creation_date' if to_do =='posts' or to_do=='' else 'date'
        return order
    def get_queryset(self):
        target_user=custom_user.objects.get(username=self.kwargs['username'])
        self.target_user=target_user
        query_set=Post_Comment.objects.filter(written_by_id=target_user.id).all() if self.kwargs['to_do'] =='comments' else\
            Post_Model.objects.filter(author_id=target_user.id).all()
        print(query_set)
        return query_set


    def get_context_data(self, **kwargs):
        contex=super().get_context_data()
        target_user=self.target_user
        self.target_user=target_user
        user:custom_user=self.request.user
        target_user_fr_list,tr=User_Friends_List.objects.get_or_create(parent_user_id=target_user.id)
        contex['status']:str='unlocked'
        contex['type']=self.kwargs['to_do']
        if target_user.get_settings().show_info_to == 'friends':
            contex['status'] ='unlocked' if target_user_fr_list.get_friends_list().users.filter(id=user.id).exists() else 'locked'
        elif target_user.get_settings().show_info_to == 'everyone':
            contex['status'] ='404' if target_user.get_block_list().contains(user) else 'unlocked'
        contex['report_form']=Report_Form(initial={'parent_list':target_user.get_report_list().id,'made_by':self.request.user.id})
        contex['target_user']=target_user
        return contex

class Unblock_User(View):
    def post(self,request):
        status=''
        try:
            user:custom_user=self.request.user
            target_user=custom_user.objects.get(username=request.POST.get('username'))
            bl_list=user.user_block_list.user_list
            bl_list.users.remove(target_user)
            bl_list.save()
            status='success'
        except:
            status='failure'

        return JsonResponse({'status':status})
class Send_Friend_Request(View):
    def get(self,request,username):
        try:
          request_list=custom_user.objects.get(username=username).get_friend_requests()
          fr_request=Friend_Request(sent_by_id=request.user.id,Parent_List_id=request_list.id)
          fr_request.save()
          return JsonResponse({'status':'succeed'})
        except Exception as e:
            print(f'error is {e}')
            return JsonResponse({'status': 'failure'})
class Accept_Friend_Request(View):
    def get(self,request):
        try:
           args=list(request.GET.keys())[0].replace('[','').replace(']','').split(',')
           username=args[0].replace('"','')
           to_do=args[1].replace('"','')
           print(username,to_do)
           user:custom_user=request.user
           target_user = custom_user.objects.get(username=username)
           if to_do =='accept':
              user_fr_list,uu=User_Friends_List.objects.get_or_create(parent_user_id=user.id)
              user_fr_list=user_fr_list.get_friends_list()
              target_user_fr_list,ll=User_Friends_List.objects.get_or_create(parent_user=target_user)
              target_user_fr_list=target_user_fr_list.get_friends_list()
              user_fr_list.users.add(target_user)
              user_fr_list.save()
              target_user_fr_list.users.add(user)
              target_user_fr_list.save()
           else:
             pass
           user.friend_request_list.friend_request_set.get(sent_by_id=target_user.id).delete()
           return JsonResponse({'status':'success'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'failure'})
class Block_User(View):
    def post(self,request):
        target_user=custom_user.objects.get(username=request.POST.get('username'))
        user:custom_user=request.user
        bl_list,bb=User_Block_List.objects.get_or_create(parent_user_id=user.id)
        if bl_list.user_list == None:
            new_list=Block_List()
            new_list.save()
            bl_list.user_list=new_list
            bl_list.save()
        bl_list.user_list.users.add(target_user)
        return redirect(reverse('Load_First_Page'))

class Show_User_Messages(ListView):
    model = Message_Groups
    template_name = 'User_Messages.html'
    paginate_by = 10
    context_object_name = 'groups'
    def get_queryset(self):
        query_set=super().get_queryset()
        query_set[0].get_messages()
        user_name=self.request.user.username


        query_set=query_set.filter(users__username=user_name).annotate(count=Count('post_forwards',filter=~Q(
            post_forwards__seen_list__users=self.request.user)))


        return query_set


class Remove_Friend(View):
    def post(self,request):
        print('i was called')
        try:
           user:custom_user=request.user
           target_user=custom_user.objects.get(username=request.POST.get('username'))
           user_list,ll=User_Friends_List.objects.get_or_create(parent_user_id=user.id)
           fr_list=user_list.get_friends_list()
           fr_list.users.remove(target_user)
           fr_list.save()
           target_user_list, ll = User_Friends_List.objects.get_or_create(parent_user_id=user.id)
           target_user_fr_list = target_user_list.get_friends_list()
           target_user_fr_list.users.remove(user)
           target_user_fr_list.save()
           return JsonResponse({'status':'succeed'})
        except:
            return JsonResponse({'status':'failure'})
class Submit_Report(View):
    def post(self,request):
        print('hi')
        frm=Report_Form(request.POST)
        user:custom_user=request.user
        target_user=User_Report_List.objects.get(id=request.POST.get('parent_list')).user
        if frm.is_valid():
            frm.save()
            bl1,b=User_Block_List.objects.get_or_create(parent_user_id=user.id)
            ls1=bl1.get_block_list()
            ls1.users.add(target_user)
            ls1.save()
            bl2, b2 = User_Block_List.objects.get_or_create(parent_user_id=user.id)
            ls2 = bl2.get_block_list()
            ls2.users.add(target_user)
            ls2.save()
            return redirect(reverse('Load_First_Page'))
        else:
            return redirect(reverse('show_user_profile',kwargs={'username':target_user.username}))

class Password_Reset:
    class Ask_For_Password_Reset(View):
        def post(self,request):
            try:
               email=request.POST.get('email')
               user=custom_user.objects.get(email=email)
               my_code=get_random_string(72)

               user.reset_pass_code=my_code
               user.save()
               result=Send_Email_To(template_name='Password_Reset_Page.html',subject= 'Reset Your Password',to=email,contex= {'reset_code':my_code})

               return JsonResponse({'status':'success' if result == 'succeed' else 'failure'})
            except Exception as e:
                print(e)
                return JsonResponse({'status':'failure'})
        def get(self,request):
            return render(request,'Ask_For_Password_Reset.html')
    class Reset_Password(View):
        def get(self,request):
            frm=Password_Reset_Form()
            act_code=request.GET.get('reset_code')
            print(request.GET.get('reset_code'))
            return render(request, 'Reset_Password.html',context={'form':frm,'reset_code':act_code})
        def post(self,request):
            frm=Password_Reset_Form(request.POST)
            res_code=request.POST.get('reset_code')
            if frm.is_valid():
                passw=frm.cleaned_data.get('password')
                passw_reset=frm.cleaned_data.get('password_repeat')
                if passw == passw_reset:
                    try:
                        print(res_code)
                        user=custom_user.objects.get(reset_pass_code=res_code)

                        user.set_password(passw)
                        user.save()
                        response=render(request,'Successfull_Password_Reset.html')
                        print('succcesssss', passw, passw_reset)
                    except Exception as e:
                        print('jumped to exception',passw,passw_reset,f'error is {e}')
                        response=render(request,'Reset_Password.html',{'form':frm,'reset_code':res_code})
                else:
                    frm.add_error('password','Passwords Dont match !')
                    response = render(request, 'Reset_Password.html', {'form': frm,'reset_code':res_code})
            else:
                response = render(request, 'Reset_Password.html', {'form': frm,'reset_code':res_code})
            return response