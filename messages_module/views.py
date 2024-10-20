from django.db.models import Q
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render
from django.views import View

from messages_module.models import Message_Groups,Message,Post_Forwards,Message_Seen_List
from user_moudle.models import custom_user


# Create your views here.
class Send_New_Message(View):
    def post(self,request:HttpRequest):
        try:
          text=request.POST.get('message_text')
          sent_by=request.user.id
          target_group=Message_Groups.objects.get(title=request.POST.get('group_title'))
          msg=Message(sent_by_id=sent_by,main_text=text,parent_group_id=target_group.id)
          msg.save()

          return JsonResponse({'status':'succeed'})
        except:
            return JsonResponse({'status': 'failure'})

class Forward_A_Post(View):
    def post(self,request):
      try:
        post_id=request.POST.get('post_id')
        sent_by=request.user.id
        ids=request.POST.getlist('targets')
        
        print(ids)
        for id in ids:
            ind=id.index(',')
            type=id[ind+1::]
            if type =='group':
                gr=Message_Groups.objects.get(title=id[0:ind:])
                Post_Forwards.objects.create(parent_group=gr,sent_by_id=sent_by,post_id=post_id).save()
            elif type == 'user':

                gr = Message_Groups.objects.filter(group_type='direct',users__username__in=[request.user.username,id[0:ind:]]).first()
                if not gr:
                    gr=Message_Groups(group_type='direct')
                    gr.save()
                    gr.users.add(request.user)
                    gr.users.add(custom_user.objects.get(username=id[0:ind:]))
                Post_Forwards.objects.create(parent_group=gr, sent_by_id=sent_by, post_id=post_id).save()
        response = {'status': 'success'}
      except Exception as e:
          print(e)
          response={'status':'failure'}
      return JsonResponse(response)



class Mark_Message_As_Seen(View):
    def post(self,request):
        print('mark messages was called')
        type=request.POST.get('m_type')
        id = request.POST.get('m_id')
        msg = Message.objects.get(id=id) if type =='message' else Post_Forwards.objects.get(id=id)
        try:
             if msg.seen_list == None:
                 lst=Message_Seen_List()
                 lst.save()
                 msg.seen_list=lst
                 msg.save()
             else:
                 lst=msg.seen_list
             lst.users.add(request.user)
             response={'status':'success'}
        except Exception as e:
            print('exception is',e)
            response = {'status': 'failure'}

        return JsonResponse(response)