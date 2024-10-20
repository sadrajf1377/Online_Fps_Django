import decimal
import json

from django.db.models import OuterRef, Exists, Count
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import Product_serializer
from .models import Product,User_Bought_Products,Product_List_Detail,Product_Comment
from user_moudle.models import custom_user
from utils.my_decorators import Unity_View
from .forms import Prdouct_Comment_Form
# Create your views here.
@api_view(['GET'])
@Unity_View
def Show_Products(request,start_number):
    if request.method == 'GET':
      print(request.headers)
      start_number1:int=int(start_number)*5
      data=Product_serializer(Product.objects.all()[start_number1:start_number1+5:1],many=True)
      return Response(data=data.data,status=200)

class Confirm_Order(View):
    def post(self,request:HttpRequest):
        try:
           #data=json.loads(request.POST.get('my_data'))
           print(json.loads(request.POST.get('my_data')))
           session_id=request.POST.get('session_id')

           user:custom_user=custom_user.objects.get(user_sessions__key=session_id)

           pr_list,pp=User_Bought_Products.objects.get_or_create(owner_id=user.id)
           ids:str=request.POST.get('ids_and_count').split(',')
           prs=list(Product.objects.filter(id__in=ids[::2]))

           counter: int = 1
           for item in prs:
             user.account_balance -= item.price * decimal.Decimal(ids[counter])
             result=user.account_balance>=0
             if not result:
                 break
             count=int(ids[counter])
             detail,dd=Product_List_Detail.objects.get_or_create(product_id=item.id,parent_list_id=pr_list.id)
             counter += 2
             detail.count+=count
             detail.save()

           if result:
              user.save()

           return JsonResponse({'result':'success' if result else 'failure'})
        except Exception as e:
            print(f'error is {e.args}')
            return JsonResponse({'result': 'failure'})


class Get_My_Products(View):
    def post(self,request):
        user=custom_user.objects.get(user_sessions__key=request.POST.get('session_id'))
        products=User_Bought_Products.objects.get(owner_id=user.id).product_list_detail_set.all()
        return JsonResponse({'products':products})

class Get_My_Products_Web(ListView):
    template_name = 'My_Products.html'
    model = Product_List_Detail
    context_object_name = 'products'
    paginate_by = 6
    def get_queryset(self):
        query_set=super().get_queryset()
        id,ii=User_Bought_Products.objects.get_or_create(owner_id=self.request.user.id)
        query_set=query_set.filter(parent_list_id=id.id)
        return query_set
class Show_Products_Web(ListView):
    model = Product
    template_name = 'Show_Products.html'
    paginate_by = 8
    ordering = 'creation_date'
    context_object_name = 'products'
    def get_queryset(self):
        query_set=super().get_queryset()
        query_set=query_set.annotate(i_own=Exists(Product_List_Detail.objects.filter(product_id=OuterRef('pk'),parent_list__owner_id=self.request.user.id)))
        return query_set

class Show_Product_Details(ListView):
    template_name = 'Prdouct_Details.html'
    model = Product_Comment
    ordering = 'creation_date'
    context_object_name = 'comments'
    paginate_by = 10
    def get_context_data(self, *, object_list=None, **kwargs):
        contex=super().get_context_data()
        contex['product']=Product.objects.get(product_name=self.kwargs['product_name'])
        contex['comment_form']=Prdouct_Comment_Form()
        return contex
    def get_queryset(self):

        query_set=super().get_queryset().filter(parent_product__product_name=self.kwargs['product_name'],parent_comment_id=None)
        query_set=query_set.annotate(is_mine=Exists(Product_Comment.objects.filter(wrote_by_id=self.request.user.id,id=OuterRef('pk'))))
        query_set=query_set.annotate(replies=Count('product_comment'))

        return query_set
class Comment_On_Product(View):
    def post(self,request:HttpRequest):
          frm=Prdouct_Comment_Form(request.POST)

          if frm.is_valid():
              try:
                  text = frm.cleaned_data.get('comment')
                  id = request.POST.get('pr_id')
                  parent_id=request.POST.get('parent_id')
                  comment=Product_Comment(comment=text, parent_product_id=id, wrote_by_id=request.user.id,parent_comment_id=parent_id
                                          if parent_id != '' else None)
                  comment.save()

                  response= JsonResponse({'status': 'success','object':{'text':comment.comment,'sent_by':comment.wrote_by.username,'date':
                                                                        comment.creation_date,'is_reply':comment.parent_comment_id != None}})
              except Exception as E:
                  print(E)
                  response=JsonResponse({'status': 'failure'})
          else:
              response = JsonResponse({'status': 'failure'})
          return response


class Delete_Comment(DeleteView):
    model = Product_Comment
    success_url = 'random'
    template_name = 'Prdouct_Details.html'
    def get_object(self, queryset=None):
        object=Product_Comment.objects.get(id=self.request.POST.get('id'))
        return object
    def post(self,request):
        print('i was called')
        try:
          super().post(request)
          return JsonResponse({'result':'success'})
        except Exception as e:
            print(e)
            return JsonResponse({'result': 'failure'})