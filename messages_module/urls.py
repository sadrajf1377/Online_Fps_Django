from django.urls import path

from .views import Send_New_Message,Mark_Message_As_Seen,Forward_A_Post

urlpatterns=[
    path('/send_message',Send_New_Message.as_view(),name='send_new_message'),

path('/forward_post',Forward_A_Post.as_view(),name='forward_post')
    ,path('/mark_as_seen',Mark_Message_As_Seen.as_view(),name='mark_as_seen')
]