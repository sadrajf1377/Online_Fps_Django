from django.db.models import Count, Q
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from .models import Report,Report_Session
from .forms import Report_form
# Create your views here.

class Fill_Report(View):
    def post(self,request:HttpRequest):
        try:
          report_frm=Report_form(request.POST,request._files)
          if report_frm.is_valid():
              report_frm.save()
              response= {'status':'success'}
          else:
             response={'status':'failure'}
        except Exception as e:
            print(e)
            response = {'status': 'failure'}
        return JsonResponse(response)
class Report_Session_Details(ListView):
    template_name = 'Report_Session_Details.html'
    paginate_by = 6
    context_object_name = 'messages'
    model = Report
    ordering = 'creation_date'
    def get_queryset(self):
        query_set=super().get_queryset()

        query_set=query_set.filter(reply_to__isnull=True,report_session__title=self.kwargs['title']).annotate(replies=Count('report'))
        return query_set
    def get_context_data(self, *, object_list=None, **kwargs):
        contex=super().get_context_data()
        contex.update({'form':Report_form()})
        contex.update({'session_id':Report_Session.objects.get(title=self.kwargs['title']).id})
        return contex

class Show_My_Reports(ListView):
    model = Report_Session
    template_name = 'My_Reports.html'
    context_object_name = 'sessions'
    paginate_by = 8
    ordering = 'date_of_creation'
    def get_queryset(self):
        query_set=super().get_queryset().filter(owner_user_id=self.request.user.id)
        query_set=query_set.annotate(replies=Count('report',filter=(Q(report__is_reply=False))))
        return query_set


class Delete_Report(DeleteView):
    model = Report
    template_name = 'Report_Session_Details.html'
    success_url = 'somewhere'
    def get_object(self, queryset=None):
        object=Report.objects.get(id=self.request.POST.get('id'))
        return object
    def post(self,request):
        try:
          print(request.POST)
          super().post(request)
          response={'status':'success'}
        except Exception as e:
            print(e)
            response = {'status': 'failure'}
        return JsonResponse(response)







class Crete_New_Session(View):
    def post(self,request):
        title=request.POST.get('title')
        Report_Session.objects.create(title=title,owner_user_id=request.user.id).save()
        return redirect(reverse('show_my_reports'))
class Delete_Session(View):
    def post(self,request):
        try:
          title=request.POST.get('title')
          Report_Session.objects.get(title=title).delete()
          response={'status':'success'}
        except:
            response={'status':'failure'}
        return JsonResponse(response)