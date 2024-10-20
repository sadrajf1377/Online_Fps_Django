import random
from sqlite3 import Date
import datetime

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.crypto import get_random_string
from utils.my_functions import Check_If_Online
from utils.Email_Sending import Send_Email_To

# Create your models here.
class custom_user(AbstractUser):
    activation_code=models.CharField(max_length=72,default='',verbose_name='Activation Code',null=False,blank=False)
    avatar=models.ImageField(upload_to='avatars/',verbose_name='user avatar',null=True)
    ranks=(('copper','copper'),('bronze','bonze'),('silver','silver'),('gold','gold'))
    user_ranking=models.CharField(max_length=10,verbose_name="user's rank",choices=ranks,default='copper')
    user_total_score=models.IntegerField(default=0,verbose_name='user score')
    kill_per_death=models.FloatField(default=0,verbose_name="user's k/d")
    birth_date=models.DateTimeField(null=True,blank=True,verbose_name='Users BirthDate')
    user_settings=models.OneToOneField('User_Settings',on_delete=models.SET_NULL,null=True)
    status_list=(('normal','normal'),('banned','banned'))
    user_status=models.CharField(choices=status_list,max_length=50,null=False,blank=False,default='normal')
    reset_pass_code=models.CharField(max_length=72,default='',null=True,blank=True,verbose_name='reset pass code')
    account_balance=models.DecimalField(verbose_name='total balance',default=0000,max_digits=8,decimal_places=4)
    def my_normal_groups(self):
        return self.message_groups_set.filter(group_type='normal').all()
    def get_report_list(self):

        lst,ll=User_Report_List.objects.get_or_create(user_id=self.id)
        return lst
    def get_friend_requests(self):
        requests,rr=Friend_Request_List.objects.get_or_create(List_Owner_id=self.id)

        return requests
    def get_avatar(self):
        try:
            url=self.avatar.url
        except:
            url=''
        return url
    def get_settings(self):

        if self.user_settings != None:

            settings=self.user_settings
        else:

            settings=User_Settings()
            settings.save()
            self.user_settings=settings
            self.save()
            print(self.username)
        return settings
    def get_friends_list(self):
        friends_list,ff=User_Friends_List.objects.get_or_create(parent_user_id=self.id)
        if friends_list.user_list == None:
            fr_list=Friends_List.objects.create()
            friends_list.user_list=fr_list
            friends_list.save()
        else:
            fr_list=friends_list.user_list
        names=str({str(x.username):str(Check_If_Online(x.username)) for x in fr_list.users.all()})
        return names


    def get_block_list(self):
        block_list,bb=User_Block_List.objects.get_or_create(parent_user_id=self.id)
        if block_list.user_list == None:
            blocked_users=Block_List.objects.create()
            block_list.user_list=blocked_users
            block_list.save()
        else:
            blocked_users=block_list.user_list

        return blocked_users.users.all()
    def __str__(self):
        print(self.avatar)


        return self.username
class User_Sessions(models.Model):
    user=models.ForeignKey(custom_user,verbose_name='Owner of session',on_delete=models.CASCADE,null=False,blank=False)
    key=models.CharField(verbose_name='Session Key',max_length=200,blank=False,null=False,unique=True)
    def Assign_key(self):
        a=make_password(self.user.first_name)
        self.key=a

class User_Block_List(models.Model):
    parent_user=models.OneToOneField(custom_user,on_delete=models.CASCADE,null=False,blank=False,verbose_name='this block list belogns to')
    user_list=models.OneToOneField('Block_List',on_delete=models.SET_NULL,verbose_name='users list',blank=True,null=True)
    def get_block_list(self):
        lst=self.user_list
        if lst == None:
            lst=Block_List()
            lst.save()
            self.user_list=lst
            self.save()
        return lst
    def __str__(self):
        return f'this block list belongs to {self.parent_user.username}'
class User_Friends_List(models.Model):
    parent_user = models.OneToOneField(custom_user, on_delete=models.CASCADE, null=False, blank=False,verbose_name='this friend list belogns to')
    user_list = models.OneToOneField('Friends_List', on_delete=models.SET_NULL, verbose_name='users list', blank=True,null=True)
    def get_friends_list(self):
        lst=self.user_list
        if lst == None:
            lst=Friends_List()
            lst.save()
            self.user_list=lst
            self.save()
        return lst
    def __str__(self):
        return f'this friends list belongs to {self.parent_user.username}'
class Friends_List(models.Model):
    users = models.ManyToManyField(custom_user, verbose_name='list of users')
    def __str__(self):
        return f'this list belongs to {self.user_friends_list.parent_user.username}'
class Block_List(models.Model):
    users=models.ManyToManyField(custom_user,verbose_name='list of users')
    def __str__(self):
        return f'this list belongs to {self.user_block_list.parent_user.username}'

class User_Settings(models.Model):
    show_choices=(('friends','friends'),('everyone','everyone'),('noone','noone'))
    show_info_to=models.CharField(default='friends',choices=show_choices,max_length=20)
    receive_messages_from=models.CharField(default='friends',choices=show_choices,max_length=20)
    who_can_befriend=models.CharField(default='friends',choices=show_choices,max_length=20)
    who_can_send_play_request=models.CharField(default='',choices=show_choices,max_length=20)
class Friend_Request_List(models.Model):
    List_Owner=models.OneToOneField(custom_user,on_delete=models.CASCADE,verbose_name='whom this list belongs to',null=False,blank=False)
    def __str__(self):
        return f'this list belongs to {self.List_Owner.username}'
class Friend_Request(models.Model):
    sent_by=models.OneToOneField(custom_user,verbose_name='sent by',on_delete=models.CASCADE,null=False,blank=False)
    Parent_List=models.ForeignKey(Friend_Request_List,verbose_name='Parent list of this request',on_delete=models.CASCADE,null=False,blank=False)
    def __str__(self):
        return f'this list belongs to {self.Parent_List.List_Owner.username}'

class User_Report(models.Model):
    reasons=(('harrasement','harrasement'),('racial_slurs','racial_slurs'),('cheating','cheating'),('racism','racism'),('other','other'))
    reason=models.CharField(max_length=15,choices=reasons,default='other',null=False,blank=False)
    made_by=models.ForeignKey(custom_user,null=False,blank=False,on_delete=models.CASCADE)
    parent_list=models.ForeignKey('User_Report_List',null=False,blank=False,on_delete=models.CASCADE)
    def __str__(self):
        return 'this report is made towards {} and is sent by {}'.format(self.parent_list.user.username,self.made_by.username)
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if User_Report.objects.filter(made_by_id=self.made_by.id,parent_list_id=self.parent_list.id).exists():
            raise ValidationError('a user cannot report another use twice')
        else:
            super().save()
            if self.parent_list.user_report_set.count()>=5:
                user=self.parent_list.user
                user.user_status ='banned'
                user.save()
                Send_Email_To(template_name='User_Ban_Announcement.html',subject='suspension',to=user.email,contex={'username':user.username})
class User_Report_List(models.Model):
    user=models.OneToOneField(custom_user,on_delete=models.CASCADE)
    def __str__(self):
        return 'this list belongs to {}'.format(self.user.username)

