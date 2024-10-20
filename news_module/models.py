from datetime import time

from django.db import models
from user_moudle.models import custom_user
# Create your models here.
from datetime import date
class News(models.Model):
    title=models.CharField(max_length=100,verbose_name='news title',default='',null=False,blank=False,unique=True,error_messages={'unique':'News instance'
                                                                                                                                           'with such title exists'})
    news_text=models.TextField(max_length=2000,verbose_name='news main text',default='',null=False,blank=False)
    image=models.FileField(upload_to='news_images/',null=False,blank=False)
    creation_date=models.DateTimeField(auto_now_add=True,verbose_name='Date of Creation',null=True)
    def get_brief(self):
        result=self.news_text[:200]

        return result
    class Meta:
        verbose_name ='News'
        verbose_name_plural='News'



class News_Comments(models.Model):
    l_or_dl_choices=(('like','like'),('dislike','dislike'),('neutral','neutral'))
    like_or_dislike=models.CharField(max_length=10,verbose_name='users opinion',choices=l_or_dl_choices,default='neutral',null=False,blank=False)
    comment=models.CharField(max_length=200,verbose_name='users comment',default='',null=False,blank=False)
    user=models.ForeignKey(custom_user,null=False,blank=False,verbose_name='Sent by',on_delete=models.CASCADE)
    parent_news=models.ForeignKey(News,null=False,blank=False,verbose_name='parent comment',on_delete=models.CASCADE)
    creation_date=models.DateTimeField(null=True,auto_now_add=True,verbose_name='creation date')
    def get_like_list(self):

        lst,ll=comment_like_list.objects.get_or_create(news_id=self.id)
        return lst
    def get_dislike_list(self):
        dslst,dsl=comment_dislike_list.objects.get_or_create(news_id=self.id)
        return dslst
    class Meta:
        verbose_name ='News Comment'
        verbose_name_plural ='News Comments'

class comment_like_list(models.Model):
    users=models.ManyToManyField(custom_user,verbose_name='users list',null=True,blank=False)
    news=models.OneToOneField(News_Comments,on_delete=models.CASCADE,null=False,blank=False,verbose_name='parent news')
class comment_dislike_list(models.Model):
    users = models.ManyToManyField(custom_user, verbose_name='users list', null=True, blank=False)
    news = models.OneToOneField(News_Comments, on_delete=models.CASCADE, null=False, blank=False, verbose_name='parent news')


