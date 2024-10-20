from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import custom_user,Friends_List,Block_List,User_Friends_List,User_Block_List,User_Settings,Friend_Request_List,Friend_Request,User_Report_List,User_Report
from messages_module.models import Message,Message_Groups
# Register your models here.
class settings(ModelAdmin):
    def get_queryset(self, request):
        print(request.session.values(),request.session.keys())
        return super().get_queryset(request)



admin.site.register(custom_user,settings)
admin.site.register(User_Friends_List)
admin.site.register(Friends_List)
admin.site.register(Block_List)
admin.site.register(User_Block_List)
admin.site.register(User_Settings)
admin.site.register(Friend_Request_List)
admin.site.register(Friend_Request)
admin.site.register(Message)
admin.site.register(Message_Groups)
admin.site.register(User_Report_List)
admin.site.register(User_Report)
