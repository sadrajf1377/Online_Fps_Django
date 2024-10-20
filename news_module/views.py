from django.db.models import Count, Exists, Q, OuterRef
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DeleteView
from .models import News,News_Comments,comment_like_list,comment_dislike_list
from user_moudle.models import custom_user
# Create your views here.
class Show_News_Details(ListView):
    model = News_Comments
    template_name = 'News_Details.html'
    context_object_name = 'comments'
    paginate_by = 10
    ordering = 'creation_date'
    def get_queryset(self):
        news_title=self.kwargs['title']
        query_set=super().get_queryset().filter(parent_news__title=news_title)
        query_set=query_set.annotate(likes=Count('comment_like_list__users')).annotate(dislikes=Count('comment_dislike_list__users'))
        query_set=query_set.annotate(i_liked=Exists(comment_like_list.objects.filter(news_id=OuterRef('pk'),users=self.request.user)))

        query_set = query_set.annotate(
            i_disliked=Exists(comment_dislike_list.objects.filter(news_id=OuterRef('pk'), users=self.request.user)))
        query_set=query_set.annotate(is_mine=Exists(News_Comments.objects.filter(id=OuterRef('pk'),user_id=self.request.user.id)))
        return query_set
    def get_context_data(self, *, object_list=None, **kwargs):
        news=News.objects.get(title=self.kwargs['title'])
        contex=super().get_context_data()
        contex['news']=news
        return contex
class Comment_On_News(View):
    def post(self,request):
        l_or_d=request.POST.get('like_or_dislike')
        comment_text=request.POST.get('comment_text')
        parent_news=News.objects.get(title=request.POST.get('parent_news'))
        user=request.user
        cmnt=News_Comments(comment=comment_text,like_or_dislike=l_or_d,user_id=user.id,parent_news_id=parent_news.id)
        cmnt.save()
        return redirect(reverse('show_news_details',args=[parent_news.title]))
class Like_or_Dislike_Comment(View):
    def post(self,request):
        try:
           id=request.POST.get('id')
           news=News_Comments.objects.get(id=id)
           to_do:str=request.POST.get('to_do')


           if to_do.__contains__('dislike'):
                print(news)
                l_list = news.get_dislike_list()
                print(l_list)
                if to_do == 'remove_dislike':

                    l_list.users.remove(request.user)
                    print('removed')
                elif to_do =='dislike':
                    l_list.users.add(request.user)
                    if request.POST.get('to_remove') == 'true':
                        l=news.get_like_list()
                        l.users.remove(request.user)
                        l.save()
                    print('added')
                l_list.save()
                response={'status': 'success'}
           elif not to_do.__contains__('dislike') and to_do.__contains__('like'):
               l_list = news.get_like_list()
               if to_do == 'like':
                   l_list.users.add(request.user)
                   if request.POST.get('to_remove') == 'true':
                       l = news.get_dislike_list()
                       l.users.remove(request.user)
                       l.save()
               elif to_do == 'remove_like':
                   l_list.users.remove(request.user)
               l_list.save()
               response = {'status': 'success'}
           else:
               response = {'status': 'failure'}
        except Exception as e:
            print(e)
            response= {'status': 'failure'}
        return JsonResponse(response)


class Remove_Comment(View):
    def post(self,request:HttpRequest):
        try:
           id=request.POST.get('id')
           News_Comments.objects.get(id=id).delete()
           response={'status':'succeed'}
        except:
            response={'status':'failure'}
        return JsonResponse(response)




