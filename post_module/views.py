from django.db.models import Count, Exists, OuterRef, Q, Value, Sum, Case, When, BooleanField
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DeleteView, DetailView, UpdateView
from .models import Post_Model, Post_Comment, Hash_Tag, Post_Images
from .forms import Comment_Form,Create_Post_Form
from user_moudle.models import custom_user

# Create your views here.
class Show_All_Posts(ListView):
    model = Post_Model
    ordering = 'creation_date'
    template_name = 'All_Posts.html'
    paginate_by = 16
    context_object_name = 'posts'
    def get_context_data(self, *, object_list=None, **kwargs):
        contex=super().get_context_data()
        contex['form']=Comment_Form()
        return contex
    def get_queryset(self):
        query_set=super().get_queryset()
        try:
            to_do=self.kwargs['group']
            if to_do == 'home':
                friends_list = list(
                    self.request.user.user_friends_list.user_list.users.all().values_list('id', flat=True))
                query_set = query_set.filter(author_id__in=friends_list)
            elif to_do == 'explore':
                user: custom_user = self.request.user
                hs = Hash_Tag.objects.annotate(
                    cnt=Count('posts', filter=Q(posts__post_like_list__users=user))).order_by(
                    '-cnt').values_list('posts', flat=True)
                hs = list(set(hs))
                order = Case(
                    *[When(pk=id, then=pos) for pos, id in enumerate(hs)]
                )
                query_set = query_set.order_by(order)
            query_set = query_set.annotate(comment_count=Count('post_comment', distinct=True),
                                           like_count=Count('post_like_list__users', distinct=True)).annotate(
                i_liked=Case(When(post_like_list__users=self.request.user,then=Value(True)),default=Value(False),output_field=BooleanField())
            ).annotate(has_picture=Case(When(post_images__isnull=True,then=Value(False)),default=True,output_field=BooleanField()))

        except:
            query_set=()
        return query_set
class Write_A_Comment(View):
    def post(self,request):
        frm=Comment_Form(request.POST)
        if frm.is_valid():
            comment=frm.save()
            response={'status':'success','message':comment.comment_text,'username':comment.written_by.username}
        else:
            response = {'status': 'failure'}
        print(frm.errors)
        return JsonResponse(response)
class Add_Or_Remove_Like(View):
    def post(self,request):
        id=request.POST.get('message_id')



        try:
          post=Post_Model.objects.get(title=request.POST.get('post_title'))

          is_liked=request.POST.get('is_liked') == '1'
          if is_liked:
              post.post_like_list.users.remove(request.user)
          else:
              post.post_like_list.users.add(request.user)
          response= {'status':'succeed'}
        except:
            response={'status':'failure'}
        return JsonResponse(response)

class Delete_Comment(View):
    def post(self, request):
        try:
            Post_Comment.objects.get(id=self.request.POST.get('id')).delete()
            response={'status':'succeed'}
        except:
            response = {'status': 'failure'}
        return JsonResponse(response)

class View_Posts_By_Hashtag(ListView):
    model = Post_Model
    template_name = 'All_Posts.html'
    context_object_name = 'posts'
    paginate_by = 12
    ordering = 'creation_date'
    def get_queryset(self):
        tag=self.kwargs['hash_tag']
        query_set=super().get_queryset()
        query_set=query_set.filter(hash_tag__title=tag)
        return query_set

class Post_Details(ListView):
    template_name = 'Post_Details.html'
    model = Post_Comment
    context_object_name = 'comments'
    paginate_by = 25
    ordering = 'date'
    def get_context_data(self, *, object_list=None, **kwargs):
        contex=super().get_context_data()
        contex['form']=Comment_Form()
        contex['post']=Post_Model.objects.get(title=self.kwargs['title'])
        return contex
    def get_queryset(self):
        query_set=super().get_queryset().filter(parent_post__title=self.kwargs['title'])\
            .annotate(is_mine=Case(When(written_by=self.request.user,then=Value(True)),default=Value(False),output_field=BooleanField()))
        return query_set

class Create_Post(View):
    def post(self,request:HttpRequest):
        files=request._files.getlist('pictures')
        frm=Create_Post_Form(request.POST)


        if frm.is_valid():
             if frm.cleaned_data.get('author').id == request.user.id:
                    pst=frm.save(commit=True)

                    for file in files:
                          img=Post_Images(picture=file,parent_post=pst)
                          img.save()
                    response = render(request, 'All_Posts.html')
             else:
              frm.add_error('caption','Invalid Author')
              response=render(request,'Create_Post.html',context={'form':frm})
        else:
            response=render(request,'Create_Post.html',context={'form':frm})
        return response


    def get(self,request):
        form=Create_Post_Form(None)
        return render(request,'Create_Post.html',context={'form':form})


class Show_My_Posts(ListView):
    model = Post_Model
    ordering = 'creation_date'
    template_name = 'My_Posts.html'
    paginate_by = 15
    context_object_name = 'posts'
    def get_queryset(self):

        query=super().get_queryset()
        query=query.filter(author_id=self.request.user.id).annotate(like_count=Count('post_like_list__users',distinct=True)).\
            annotate(comment_count=Count('post_comment')).annotate(has_pic=Case(When(post_images__isnull=False,then=Value(True)),default=False,output_field=
                                                                                BooleanField()))
        return query


class Delete_Post(DeleteView):
    model = Post_Model
    template_name = 'My_Posts.html'
    success_url = 'sth'

    def get_object(self, queryset=None):
        obj=Post_Model.objects.get(id=self.kwargs['post_id'],author_id=self.request.user.id)
        return obj
    def post(self, request, *args, **kwargs):
        try:
            super().post(request)
            response=JsonResponse({'status':'success'})
        except:
            response = JsonResponse({'status': 'failure'})
        return response
class Request_Post_Details(View):
    def post(self,request):
        id=request.POST.get('post_id')
        post=Post_Model.objects.get(id=id)
        pics=[x.picture.url for x in post.post_images_set.all()]
        comments = list(Post_Comment.objects.filter(parent_post_id=request.POST.get('post_id')).order_by('date'))[0:5:]
        has_next = len(comments) == 5
        comments.pop()
        comments=[[x.written_by.username,x.comment_text] for x in comments]

        data={'pictures':pics,'comments':comments,'has_next':has_next}
        return JsonResponse({'result':data})



class Load_Post_Comments(View):
    def post(self,request):
        start =int(request.POST.get('start'))
        comments=list(Post_Comment.objects.filter(parent_post_id=request.POST.get('post_id'),parent_post__author=request.user)
                      .order_by('date'))[start:start+5:]
        has_next=len(comments)==5
        if has_next:
          comments.pop()
        result=[[x.written_by.username,x.comment_text] for x in comments]
        print(start,comments)
        return JsonResponse({'result':result,'has_next':has_next})

class Edit_Post(UpdateView):
    template_name = 'Edit_Posts.html'
    model = Post_Model
    fields=['caption','title']
    context_object_name = 'form'
    success_url = ''
    def post(self,request):
        super().post(request)
        imgs_to_delete=request.POST.get('imgs_to_delete').split(',')
        parent_post=self.get_object()
        Post_Images.objects.filter(parent_post__author_id=self.request.id,parent_post=parent_post,id__in=imgs_to_delete).delete()
        imgs_to_add=request.POST.FILES.getlist('new_imgs')
        for img in imgs_to_add:
            im=Post_Images(parent_post=parent_post,picture=img)
            im.save()
        return self.get(request)
    def get_object(self, queryset=None):
        obj=Post_Model.objects.get(title=self.kwargs['title'])
        return obj

