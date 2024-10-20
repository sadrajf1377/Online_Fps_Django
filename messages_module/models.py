from django.core.exceptions import ValidationError
from django.db import models
from user_moudle.models import custom_user
from post_module.models import Post_Model
# Create your models here.
class Message_Seen_List(models.Model):
    users=models.ManyToManyField(custom_user,null=True,blank=True)

class Message_Groups(models.Model):
    users=models.ManyToManyField(custom_user,null=True,verbose_name='groups users',blank=True)
    title=models.CharField(max_length=20,verbose_name='title of this group',default='')
    types=(('normal','normal'),('direct','direct'))
    group_type = models.CharField(max_length=10,choices=types,default='normal',verbose_name='type of group')


    def get_messages(self):
        print('solam')
        messages=self.message_set.all()
        posts=self.post_forwards_set.all()
        query_set=[]
        query_set.extend(list(messages))
        query_set.extend(list(posts))
        print(query_set)
        query_set=sorted(query_set,key=lambda x:x.date)
        query_set.reverse()

        return query_set



class Message(models.Model):
    sent_by=models.ForeignKey(custom_user,on_delete=models.CASCADE,verbose_name='sent by who',null=False,blank=False)
    parent_group=models.ForeignKey(Message_Groups,on_delete=models.CASCADE,null=False,blank=False,verbose_name='parent message group',db_index=True)
    date=models.DateTimeField(auto_now_add=True,verbose_name='when this message was created')
    main_text=models.CharField(max_length=1000,verbose_name='message main text',null=False,blank=False)
    types = (('normal', 'normal'), ('post', 'post'))
    message_type = models.CharField(max_length=10, choices=types, null=False, blank=False,default='normal')
    image = models.ImageField(upload_to='group_messages', null=True, blank=True, verbose_name='attached image')



    seen_list=models.OneToOneField(Message_Seen_List,on_delete=models.SET_NULL,null=True,blank=True)

    def save(self,**kwargs):
        sent_by=self.sent_by
        group=self.parent_group
        if not group.users.contains(sent_by):
            raise ValueError('user is not in this group')
        else:

            super().save(**kwargs)



class Post_Forwards(models.Model):
    post=models.ForeignKey(Post_Model,on_delete=models.CASCADE,null=False,blank=False,verbose_name='attached post')
    parent_group=models.ForeignKey(Message_Groups,on_delete=models.CASCADE,null=False,blank=False,verbose_name='which group does this message belong to')
    sent_by=models.ForeignKey(custom_user,on_delete=models.CASCADE,null=False,blank=False,verbose_name='who sent this post')
    date=models.DateTimeField(auto_now_add=True,verbose_name='date of creation')
    desc=models.TextField(max_length=500,null=True,blank=True,verbose_name='posts description')
    seen_list = models.OneToOneField(Message_Seen_List, on_delete=models.SET_NULL, null=True, blank=True)





